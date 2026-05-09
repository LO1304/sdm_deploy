#!/usr/bin/env bash
# ══════════════════════════════════════════════
# SDM Mouride — Script de build pour Render
# ══════════════════════════════════════════════
set -o errexit

echo "═══ Installation des dépendances ═══"
pip install --upgrade pip
pip install -r requirements.txt

echo "═══ Migrations de la base de données ═══"
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "═══ Collecte des fichiers statiques ═══"
python manage.py collectstatic --noinput

echo "═══ Création du superutilisateur (si demandé) ═══"
if [ "$CREATE_SUPERUSER" = "true" ]; then
  python manage.py createsuperuser --no-input --username "moustapha" --email "cheikhmouhamadoumoustaphalo@gmail.com" || true
fi

echo "═══ Build terminé avec succès ! ═══"