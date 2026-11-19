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

echo "═══ Enrichissement pédagogique Tazawwudu-ç-Çighâr ═══"
if [ -f "enrich_grandes_etapes.py" ]; then
    python enrich_grandes_etapes.py
fi
if [ -f "enrich_paid_revisions.py" ]; then
    python enrich_paid_revisions.py
fi

echo "═══ Nettoyage des anciens fichiers statiques ═══"
rm -rf staticfiles_build

echo "═══ Collecte des fichiers statiques ═══"
python manage.py collectstatic --noinput --clear

echo "═══ Création/Mise à jour des administrateurs ═══"
# ON NE LANCE PLUS AUTOMATIQUEMENT LE SCRIPT EN PRODUCTION
# python force_admin.py

echo "🔥 Création des Sessions de Zikr par défaut 🔥"
# ON NE LANCE PLUS AUTOMATIQUEMENT LE SCRIPT EN PRODUCTION (Lock SQLite)
# python manage.py shell -c "exec(open('populate_sessions.py', encoding='utf-8').read()); run()"

echo "🔥 Nettoyage & Déploiement des Sons Vérifiés (Base de données) 🔥"
python deploy_sons.py

echo "🔥 Enrichissement Audiothèque (~600 Sons : Khassidas, Coran, Xam Xam, Wakhtane) & 30 Jukkis Coran 🔥"
python enrich_audiotheque.py

echo "═══ Build terminé avec succès ! ═══"