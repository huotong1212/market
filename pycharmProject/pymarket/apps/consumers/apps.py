from django.apps import AppConfig


class ConsumersConfig(AppConfig):
    name = 'consumers'

    def ready(self):
        import consumers.signals