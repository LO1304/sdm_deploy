"""
Script pour:
1. Supprimer les Khassidas sans PDF (ajoutees par erreur)
2. Ajouter les sons Xam Xam depuis le RSS feed de daaraykhassida.com/podcloud
"""
import os, sys, re
import xml.etree.ElementTree as ET
import requests
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from bibliotheque.models import Khassida, Son

# ── ETAPE 1: Supprimer les Khassidas sans fichier PDF ──
empty_khassidas = Khassida.objects.filter(fichier_pdf='')
count_deleted = empty_khassidas.count()
empty_khassidas.delete()
print(f"[1/2] Supprime {count_deleted} Khassidas sans PDF.")
print(f"       Khassidas restants: {Khassida.objects.count()}")

# ── ETAPE 2: Ajouter les sons Xam Xam depuis le RSS ──
rss_url = 'https://khassida.lepodcast.fr/rss'
print(f"\n[2/2] Telechargement du RSS: {rss_url}")

try:
    resp = requests.get(rss_url, timeout=15)
    resp.raise_for_status()
except Exception as e:
    print(f"Erreur RSS: {e}")
    sys.exit(1)

# Parse XML
root = ET.fromstring(resp.content)
channel = root.find('channel')

# Namespace for itunes
ns = {'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}

items = channel.findall('item')
print(f"   Trouve {len(items)} episodes dans le RSS")

added = 0
skipped = 0
for item in items:
    title_el = item.find('title')
    if title_el is None or not title_el.text:
        continue
    title = title_el.text.strip()
    
    # Get audio URL from enclosure
    enclosure = item.find('enclosure')
    if enclosure is None:
        continue
    audio_url = enclosure.get('url', '')
    if not audio_url:
        continue
    
    # Get author
    author_el = item.find(f'{{{ns["itunes"]}}}author')
    if author_el is None:
        creator_el = item.find('{http://purl.org/dc/elements/1.1/}creator')
        author = creator_el.text.strip() if creator_el is not None and creator_el.text else 'Serigne Abdou Rahmane Mbacke'
    else:
        author = author_el.text.strip() if author_el.text else 'Serigne Abdou Rahmane Mbacke'
    
    # Check if already exists
    exists = Son.objects.filter(titre__iexact=title, categorie='XAM_XAM').exists()
    if exists:
        skipped += 1
        continue
    
    Son.objects.create(
        titre=title,
        auteur_voix=author,
        categorie='XAM_XAM',
        lien_audio_externe=audio_url,
        est_premium=False
    )
    added += 1

print(f"   Ajoute: {added} sons Xam Xam")
print(f"   Deja existants (ignores): {skipped}")
print(f"   Total Sons: {Son.objects.count()}")
print(f"   Total Sons Xam Xam: {Son.objects.filter(categorie='XAM_XAM').count()}")
print("\nTermine!")
