from base64 import b64encode
from io import BytesIO
from math import sqrt
from typing import Union

import segno
from cms.models.fields import PageField
from cms.models.pluginmodel import CMSPlugin
from colorfield.fields import ColorField
from django.db import models
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField
from PIL import Image
from segno.utils import get_symbol_size

MAX_RELATIVE_LOGO_SIZE = dict(L=0.05, M=0.10, Q=0.15, H=0.20)


class QRCodeBase(CMSPlugin):
    error = models.CharField(
        _("error correction level"),
        default="L",
        choices=(
            ("L", _("recovers 7% of data")),
            ("M", _("recovers 15% of data")),
            ("Q", _("recovers 25% of data")),
            ("H", _("recovers 30% of data")),
        ),
        max_length=1,
    )
    version = models.PositiveSmallIntegerField(
        _("version"),
        blank=True,
        choices=((None, _("auto")),) + tuple((n, str(n)) for n in range(1, 41)),
        null=True,
    )
    mode = models.CharField(
        _("mode"),
        blank=True,
        choices=(
            (None, _("auto")),
            ("numeric", _("numeric")),
            ("alphanumeric", _("alphanumeric")),
            ("byte", _("byte")),
            ("kanji", _("kanji")),
            ("hanzi", _("hanzi")),
        ),
        max_length=15,
        null=True,
    )
    mask = models.PositiveSmallIntegerField(
        _("data mask"),
        blank=True,
        choices=((None, _("auto")),) + tuple((n, str(n)) for n in range(8)),
        null=True,
    )
    scale = models.PositiveSmallIntegerField(_("scale"), default=10)
    border = models.PositiveSmallIntegerField(_("border"), blank=True, null=True)
    dark = ColorField(_("dark color"), blank=True, null=True)
    light = ColorField(_("light color"), blank=True, null=True)
    quiet_zone = ColorField(_("border color"), blank=True, null=True)
    alignment_dark = ColorField(_("alignment dark color"), blank=True, null=True)
    alignment_light = ColorField(_("alignment light color"), blank=True, null=True)
    finder_dark = ColorField(_("finder dark color"), blank=True, null=True)
    finder_light = ColorField(_("finder light color"), blank=True, null=True)
    logo = FilerImageField(
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name=_("logo"),
    )
    background = FilerImageField(
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name=_("background"),
    )

    class Meta:
        abstract = True

    def get_content(self, request: HttpRequest) -> Union[str, bytes]:
        raise NotImplementedError()

    def get_png_data_uri(self, request: HttpRequest) -> str:
        qrcode = segno.make(
            content=self.get_content(request),
            error=self.error,
            version=self.version,
            mode=self.mode,
            mask=self.mask,
        )
        kwargs = dict(kind="png", scale=self.scale)
        for attr in (
            "border",
            "dark",
            "light",
            "quiet_zone",
            "alignment_dark",
            "alignment_light",
            "finder_dark",
            "finder_light",
        ):
            value = getattr(self, attr)
            if value is not None:
                kwargs[attr] = value
        buffer = BytesIO()
        if self.background:
            qrcode.to_artistic(
                background=self.background.file.open(), target=buffer, **kwargs
            )
        else:
            qrcode.save(buffer, **kwargs)
        if self.logo:
            buffer.seek(0)
            qr_image = Image.open(buffer).convert("RGB")
            qr_size = get_symbol_size(
                (len(qrcode.matrix[0]), len(qrcode.matrix)), scale=1, border=0
            )[0]
            logo_size = int(
                sqrt(
                    (qr_size * qr_size - 3 * 64 - 25)
                    * MAX_RELATIVE_LOGO_SIZE[qrcode.error]
                )
            )
            # logo size and qr size must both even or both odd
            if qr_size % 2 != logo_size % 2:
                logo_size -= 1
            logo_image = Image.open(self.logo.file.open()).resize(
                (logo_size * self.scale, logo_size * self.scale)
            )
            position = (qr_image.size[0] - logo_image.size[0]) // 2
            qr_image.paste(logo_image, (position, position))
            buffer = BytesIO()
            qr_image.save(buffer, format="png")
        return "data:image/png;base64,{0}".format(
            b64encode(buffer.getvalue()).decode("ascii")
        )


class QRCode(QRCodeBase):
    content = models.TextField(_("content"), blank=True)

    def get_content(self, request: HttpRequest) -> Union[str, bytes]:
        return self.content


class QRPageLink(QRCodeBase):
    page = PageField(on_delete=models.PROTECT, related_name="+", verbose_name=_("page"))

    def get_content(self, request: HttpRequest) -> Union[str, bytes]:
        return request.build_absolute_uri(self.page.get_absolute_url())


class QRFileLink(QRCodeBase):
    file = FilerFileField(
        on_delete=models.PROTECT, related_name="+", verbose_name=_("file")
    )

    def get_content(self, request: HttpRequest) -> Union[str, bytes]:
        return request.build_absolute_uri(self.file.get_absolute_url())
