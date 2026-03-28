#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py migrate

# Collecte des fichiers statiques pour WhiteNoise et Cloudinary
python manage.py collectstatic --no-input

# Création de l'admin (remplace par tes infos)
if [ "$CREATE_SUPERUSER" ]; then
  python manage.py createsuperuser --no-input --username "moustapha" --email "cheikhmouhamadoumoustaphalo@gmail.com"
fi