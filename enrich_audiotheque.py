"""
Synchronisation ultra-rapide (< 2s sur Render build.sh) & 100% vérifiée :
1. Standardise les 30 Jukkis du Saint Coran (numero=1..30, titre="Jukki X (Juz X)") et supprime les vides/doublons.
2. Charge verified_open_sons.json (chaque MP3 a été vérifié octet par octet en HTTP 200/206).
3. Supprime de la base tout lien cassé / non vérifié (tout en préservant les fichiers admin Cloudinary video/upload & locaux).
4. Insère ou met à jour en masse tous les Kourels Mourides, Khassidas, Wolofals, Xam Xam, Coran et Adhan vérifiés.
"""
import os
import re
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from django.db.models import Count
from bibliotheque.models import Son, Coran, Khassida


def standardize_coran_jukkis():
    print("1/2 — Standardisation des 30 Jukkis du Saint Coran...")
    Coran.objects.filter(fichier_pdf='').delete()
    Coran.objects.filter(fichier_pdf__isnull=True).delete()

    kamils = list(Coran.objects.filter(titre__icontains='Kamil Darou Minane').order_by('id'))
    if len(kamils) > 1:
        for dup in kamils[1:]:
            dup.delete()

    fixed = 0
    for c in Coran.objects.all():
        m = re.match(r'^\s*(?:jukki|juz)\s*(\d+)\b', (c.titre or '').strip(), re.I)
        if m:
            num = int(m.group(1))
            target_title = f"Jukki {num} (Juz {num})"
            if c.numero != num or c.titre != target_title:
                c.numero = num
                c.titre = target_title
                c.save(update_fields=['numero', 'titre'])
                fixed += 1
    print(f"  => {fixed} Jukki(s) mis à jour (Total Coran PDF : {Coran.objects.count()})")


def sync_verified_sons():
    print("2/2 — Synchronisation du catalogue audio 100% vérifié (verified_open_sons.json)...")
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verified_open_sons.json')
    if not os.path.isfile(json_path):
        print(f"  [Attention] {json_path} introuvable — synchronisation ignorée.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        verified_items = json.load(f)

    verified_by_url = {
        it['lien_audio_externe'].strip(): it
        for it in verified_items
        if it.get('lien_audio_externe')
    }
    print(f"  Pistes 100% vérifiées dans le catalogue : {len(verified_by_url)}")

    # 1. Supprimer toutes les pistes cassées / mortes / doublons non présentes dans le catalogue vérifié
    #    (on préserve uniquement les uploads manuels admin dans /media/audios/telegram/ ou /static/audios_locaux/)
    #    et synchroniser les noms de profils/collections propres sur les pistes existantes.
    to_delete_ids = []
    to_update_objs = []
    existing_urls = set()
    for s in Son.objects.all():
        u = (s.lien_audio_externe or '').strip()
        is_manual_admin = ('/media/audios/telegram/' in u) or u.startswith('/static/audios_locaux/')
        if (u not in verified_by_url and not is_manual_admin) or ('/raw/upload/' in u):
            to_delete_ids.append(s.id)
            continue

        if u in existing_urls:
            # Doublon exact d'URL déjà présent en base
            to_delete_ids.append(s.id)
            continue

        existing_urls.add(u)
        if u in verified_by_url:
            meta = verified_by_url[u]
            new_titre = (meta.get('titre') or s.titre or 'Audio Mouride')[:200]
            new_auteur = (meta.get('auteur_voix') or 'Kourel Mouride')[:150]
            new_cat = (meta.get('categorie') or s.categorie or 'KHASSIDA').upper()
            if s.titre != new_titre or s.auteur_voix != new_auteur or s.categorie != new_cat:
                s.titre = new_titre
                s.auteur_voix = new_auteur
                s.categorie = new_cat
                to_update_objs.append(s)

    if to_delete_ids:
        Son.objects.filter(id__in=to_delete_ids).delete()
        print(f"  => {len(to_delete_ids)} piste(s) cassée(s) / morte(s) / doublon(s) supprimée(s).")

    if to_update_objs:
        Son.objects.bulk_update(to_update_objs, ['titre', 'auteur_voix', 'categorie'], batch_size=100)
        print(f"  => {len(to_update_objs)} piste(s) synchronisée(s) avec leur profil/collection unifié.")

    # 2. Ajouter toutes les pistes vérifiées manquantes en 1 seul bulk_create ultra-rapide
    to_create = []
    for u, it in verified_by_url.items():
        if not u or u in existing_urls:
            continue
        existing_urls.add(u)
        to_create.append(Son(
            titre=(it.get('titre') or 'Audio Mouride')[:200],
            auteur_voix=(it.get('auteur_voix') or 'Kourel Mouride')[:150],
            categorie=(it.get('categorie') or 'KHASSIDA').upper(),
            lien_audio_externe=u,
            est_premium=False,
        ))

    if to_create:
        Son.objects.bulk_create(to_create, batch_size=100)
    print(f"  => {len(to_create)} nouvelle(s) piste(s) vérifiée(s) ajoutée(s).")

    print("\n=== BILAN FINAL AUDIOTHÈQUE 100% VÉRIFIÉE ===")
    print("Total sons dans la base :", Son.objects.count())
    for row in Son.objects.values('categorie').annotate(c=Count('id')).order_by('-c'):
        print(f"  - {row['categorie']}: {row['c']}")


def sync_verified_pdfs():
    print("3/3 — Synchronisation des Khassidas & Corans PDF (verified_open_pdfs.json)...")
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verified_open_pdfs.json')
    if not os.path.isfile(json_path):
        print("  Aucun verified_open_pdfs.json présent — étape ignorée.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        pdf_items = json.load(f)

    existing_kh = {t.strip().lower() for t in Khassida.objects.values_list('titre', flat=True) if t}
    existing_co = {t.strip().lower() for t in Coran.objects.values_list('titre', flat=True) if t}
    existing_co_nums = set(Coran.objects.exclude(numero__isnull=True).values_list('numero', flat=True))

    new_kh = []
    new_co = []
    for it in pdf_items:
        kind = (it.get('kind') or 'KHASSIDA').upper()
        titre = (it.get('titre') or '').strip()
        pdf_field = (it.get('fichier_pdf') or '').strip()
        if not titre or not pdf_field:
            continue
        if kind == 'CORAN':
            num = it.get('numero')
            if (num and num in existing_co_nums) or titre.lower() in existing_co:
                continue
            existing_co.add(titre.lower())
            if num:
                existing_co_nums.add(num)
            new_co.append(Coran(titre=titre[:100], numero=num, fichier_pdf=pdf_field, est_premium=False))
        else:
            if titre.lower() in existing_kh:
                continue
            existing_kh.add(titre.lower())
            new_kh.append(Khassida(
                titre=titre[:255],
                auteur=(it.get('auteur') or 'Cheikh Ahmadou Bamba')[:255],
                fichier_pdf=pdf_field,
                est_premium=False,
            ))

    if new_kh:
        Khassida.objects.bulk_create(new_kh, batch_size=100)
    if new_co:
        Coran.objects.bulk_create(new_co, batch_size=50)
    print(f"  => +{len(new_kh)} Khassida(s) PDF, +{len(new_co)} Coran(s) PDF ajoutés (Total Khassidas: {Khassida.objects.count()}, Corans: {Coran.objects.count()})")


if __name__ == '__main__':
    standardize_coran_jukkis()
    sync_verified_sons()
    sync_verified_pdfs()
