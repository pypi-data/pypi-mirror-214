from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ArtdLocationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("ArtD Location")
    name = "artd_location"
