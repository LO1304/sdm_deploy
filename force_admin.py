import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from django.contrib.auth.models import User

def force_user(username, password, email):
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.is_active = True
    user.save()
    if created:
        print(f"✅ Utilisateur '{username}' CRÉÉ avec succès !")
    else:
        print(f"✅ Utilisateur '{username}' MIS À JOUR avec succès !")

if __name__ == "__main__":
    # MOT DE PASSE DE SECOURS FIXE
    FIXED_PASSWORD = "SdmMouride2026!"
    
    force_user('moustapha', FIXED_PASSWORD, 'cheikhmouhamadoumoustaphalo@gmail.com')
    force_user('admin', FIXED_PASSWORD, 'admin@example.com')
    
    print(f"\n🚀 TENTEZ DE VOUS CONNECTER AVEC :")
    print(f"Utilisateur : admin")
    print(f"Mot de passe : {FIXED_PASSWORD}")
