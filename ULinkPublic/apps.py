from django.apps import AppConfig


class UlinkpublicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ULinkPublic'

    def ready(self):
        from ULinkPublic import signals
