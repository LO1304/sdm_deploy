import os
import json
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model, login
from django.views.decorators.csrf import csrf_exempt

# --- INITIALISATION DE FIREBASE ---
def init_firebase():
    if not firebase_admin._apps:
        # Essayer de lire depuis une variable d'environnement (pour Railway)
        firebase_env = os.environ.get('FIREBASE_CREDENTIALS')
        key_path = os.path.join(settings.BASE_DIR, 'firebase-key.json')
        
        if firebase_env:
            cred_dict = json.loads(firebase_env)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        elif os.path.exists(key_path):
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
        else:
            print("ATTENTION: firebase-key.json introuvable et FIREBASE_CREDENTIALS non défini.")

init_firebase()

User = get_user_model()

@csrf_exempt
def firebase_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_token = data.get('id_token')
            
            if not id_token:
                return JsonResponse({'error': 'Token manquant'}, status=400)
                
            # Vérifier le token avec Firebase
            decoded_token = firebase_auth.verify_id_token(id_token)
            uid = decoded_token.get('uid')
            email = decoded_token.get('email', '')
            phone = decoded_token.get('phone_number', '')
            
            # Déterminer un username (on utilise l'email ou le téléphone ou l'uid)
            username = email.split('@')[0] if email else phone
            if not username:
                username = f"user_{uid[:6]}"
                
            # Créer ou récupérer l'utilisateur dans Django
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.email = email
                user.set_unusable_password()
                user.save()
                
            # Connecter l'utilisateur pour la session actuelle
            login(request, user)
            
            return JsonResponse({'success': True, 'redirect_url': '/'})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)
            
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
