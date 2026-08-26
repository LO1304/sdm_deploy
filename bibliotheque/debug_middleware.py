import logging
from django.shortcuts import render
from django.db import OperationalError, InterfaceError

logger = logging.getLogger(__name__)

class GlobalDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        # Log l'erreur côté serveur pour le débug
        logger.error(f"Erreur globale interceptée : {str(exception)}", exc_info=True)
        
        # Si c'est une erreur de base de données
        if isinstance(exception, (OperationalError, InterfaceError)):
            context = {
                'titre': 'Maintenance en cours',
                'message': 'Notre base de données redémarre ou est temporairement inaccessible. Veuillez rafraîchir la page dans quelques secondes.'
            }
            return render(request, '500.html', context, status=503)
            
        # Pour toutes les autres erreurs, afficher la page 500 classique
        return render(request, '500.html', status=500)
