#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Créer les fichiers de migration s'il y a de nouveaux changements
python manage.py makemigrations
python manage.py migrate

# Collecte des fichiers statiques pour WhiteNoise et Cloudinary
python manage.py collectstatic --no-input

# Création de l'admin (avec mot de passe sécurisé)
if [ "$CREATE_SUPERUSER" ]; then
  export DJANGO_SUPERUSER_PASSWORD="Lo13042002"
  python manage.py createsuperuser --no-input --username "moustapha" --email "cheikhmouhamadoumoustaphalo@gmail.com"
fi