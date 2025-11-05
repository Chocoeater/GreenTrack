from django.apps import AppConfig

class ConfigConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'

    def ready(self):
        import django_celery_beat
        django_celery_beat.apps.DjangoCeleryBeatConfig.ready(self)