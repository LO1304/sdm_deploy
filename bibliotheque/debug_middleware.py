import logging
from django.shortcuts import render
from django.db import OperationalError, InterfaceError
from django.core import signing
from django.contrib.auth import login, get_user_model

logger = logging.getLogger(__name__)

PERSISTENT_AUTH_SALT = 'sdm_persistent_auth_v1'
PERSISTENT_AUTH_MAX_AGE = 60 * 60 * 24 * 365 * 50  # 50 ans (Permanent / Sans expiration)


def create_persistent_auth_token(user_id):
    return signing.dumps({'uid': int(user_id)}, salt=PERSISTENT_AUTH_SALT)


def verify_persistent_auth_token(token):
    if not token:
        return None
    try:
        # Aucune limite max_age : le jeton signé reste valide de façon permanente tant que l'utilisateur ne se déconnecte pas
        data = signing.loads(token, salt=PERSISTENT_AUTH_SALT)
        return data.get('uid')
    except Exception:
        return None


class PersistentAuthMiddleware:
    """
    Garde l'utilisateur connecté pendant 365 jours même après fermeture
    complète de l'application mobile (Android / iOS / WebView / PWA).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_logout = request.path.startswith('/logout')

        if not is_logout and hasattr(request, 'user') and not request.user.is_authenticated:
            token = (
                request.COOKIES.get('sdm_remember_token')
                or request.headers.get('X-SDM-Auth-Token')
                or request.GET.get('sdm_token')
            )
            uid = verify_persistent_auth_token(token)
            if uid:
                try:
                    User = get_user_model()
                    user = User.objects.filter(id=uid, is_active=True).first()
                    if user:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        request.session.set_expiry(PERSISTENT_AUTH_MAX_AGE)
                except Exception:
                    pass

        response = self.get_response(request)

        if is_logout:
            response.delete_cookie('sdm_remember_token')
        elif hasattr(request, 'user') and request.user.is_authenticated:
            if not request.COOKIES.get('sdm_remember_token'):
                try:
                    token = create_persistent_auth_token(request.user.id)
                    response.set_cookie(
                        'sdm_remember_token',
                        token,
                        max_age=PERSISTENT_AUTH_MAX_AGE,
                        httponly=False,
                        samesite='Lax',
                    )
                except Exception:
                    pass

        return response


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
