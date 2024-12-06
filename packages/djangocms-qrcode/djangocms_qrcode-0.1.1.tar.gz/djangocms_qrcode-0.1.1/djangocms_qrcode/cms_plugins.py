from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from .models import QRCode, QRCodeBase, QRFileLink, QRPageLink


class QRCodePluginBase(CMSPluginBase):
    module = _("QR Codes")
    text_enabled = True
    render_template = "djangocms-qrcode.html"

    def render(self, context, instance: QRCodeBase, placeholder):
        context = super().render(context, instance, placeholder)
        context["content"] = instance.get_content(context["request"])
        context["png_data_uri"] = instance.get_png_data_uri(context["request"])
        return context


@plugin_pool.register_plugin
class QRCodePlugin(QRCodePluginBase):
    model = QRCode
    name = _("Simple QR Code")


@plugin_pool.register_plugin
class QRFileLinkPlugin(QRCodePluginBase):
    model = QRFileLink
    name = _("Link to a file")


@plugin_pool.register_plugin
class QRPageLinkPlugin(QRCodePluginBase):
    model = QRPageLink
    name = _("Link to a page")
