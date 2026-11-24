from django.apps import AppConfig


class BibliothequeConfig(AppConfig):
    name = 'bibliotheque'

    def ready(self):
        import bibliotheque.signals
        try:
            from bibliotheque.webpush_utils import start_background_push_worker
            start_background_push_worker()
        except Exception:
            pass
