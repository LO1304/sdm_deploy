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

echo "═══ Nettoyage des anciens fichiers statiques ═══"
rm -rf staticfiles_build

echo "═══ Collecte des fichiers statiques ═══"
python manage.py collectstatic --noinput --clear

echo "═══ Création/Mise à jour des administrateurs ═══"
python force_admin.py

echo "═══ Build terminé avec succès ! ═══"