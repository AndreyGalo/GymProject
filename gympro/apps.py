from django.apps import AppConfig


class GymproConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gympro'

    def ready(self):
        import gympro.signals

