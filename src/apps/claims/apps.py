from django.apps import AppConfig


class Config(AppConfig):
    name = 'apps.claims'
    verbose_name = 'Claims'

    def ready(self):
        import apps.claims.signal_handlers  # noqa: F401