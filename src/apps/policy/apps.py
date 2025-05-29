from django.apps import AppConfig


class Config(AppConfig):
    name = 'apps.policy'
    verbose_name = 'Policies'

    def ready(self):
        import apps.policy.signal_handlers  # noqa: F401
