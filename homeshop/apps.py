from django.apps import AppConfig


class HomeshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'homeshop'

    def ready(self):
        import homeshop.signals