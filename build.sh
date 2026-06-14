#!/usr/bin/env bash
# exit on error
set -o errexit

echo "═══ Installation des dépendances ═══"
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "═══ Migrations de la base de données ═══"
python manage.py migrate --noinput

echo "═══ Chargement des données locales ═══"
if [ -f "data_dump.json" ]; then
    python manage.py loaddata data_dump.json
fi

echo "═══ Nettoyage des anciens fichiers statiques ═══"
rm -rf staticfiles_build

echo "═══ Collecte des fichiers statiques ═══"
python manage.py collectstatic --noinput --clear

echo "═══ Création/Mise à jour des administrateurs ═══"
# ON NE LANCE PLUS AUTOMATIQUEMENT LE SCRIPT EN PRODUCTION
# python force_admin.py

echo "═══ Création des Sessions de Zikr par défaut ═══"
python manage.py shell -c "exec(open('populate_sessions.py', encoding='utf-8').read()); run()"

# ON NE LANCE PLUS l'importation lourde ici pour éviter de bloquer Render
# On le fera manuellement ou via une tâche de fond.
# python import_data.py 

echo "═══ Build terminé avec succès ! ═══"