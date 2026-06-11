from django.apps import AppConfig

class ChesshubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chesshub'

    def ready(self):
        import chesshub.signals
