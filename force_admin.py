import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from django.contrib.auth.models import User

def create_user(username, password, email):
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"✅ Utilisateur '{username}' créé avec succès !")
    else:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"✅ Mot de passe de '{username}' mis à jour !")

if __name__ == "__main__":
    # On crée les deux pour être sûr
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Lo13042002')
    create_user('moustapha', password, 'cheikhmouhamadoumoustaphalo@gmail.com')
    create_user('admin', password, 'admin@example.com')
