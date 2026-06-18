from django.apps import AppConfig


class BibliothequeConfig(AppConfig):
    name = 'bibliotheque'

    def ready(self):
        import bibliotheque.signals
