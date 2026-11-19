"""
Enrichit l'Audiothèque SDM Mouride directement dans Supabase :
1. 114 Sourates complètes du Saint Coran (Cheikh Mishary Alafasy — HTTP 200 direct, 0 octet Cloudinary)
2. 117 Enseignements Xam Xam Mourides (Tasawudu Sighaar, Masaalikul Jinaan, Tasawudu Chuban... — HTTP 200 direct, 0 octet Cloudinary)
3. Fichiers audio locaux présents dans media/audios/ (Rajass, Adhan, Khassidas manquants) uploadés sur Cloudinary (video/upload) avec fallback local
"""
import os
import re
import glob
import shutil
import requests
import xml.etree.ElementTree as ET
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from django.conf import settings
from bibliotheque.models import Son

SOURATES_114 = [
    (1, "Al-Fatiha (L'Ouverture)"), (2, "Al-Baqara (La Vache)"), (3, "Al-Imran (La Famille d'Imran)"),
    (4, "An-Nisa (Les Femmes)"), (5, "Al-Ma'ida (La Table Servie)"), (6, "Al-An'am (Les Bestiaux)"),
    (7, "Al-A'raf (Les Murailles)"), (8, "Al-Anfal (Le Butin)"), (9, "At-Tawba (Le Repentir)"),
    (10, "Yunus (Jonas)"), (11, "Hud"), (12, "Yusuf (Joseph)"), (13, "Ar-Ra'd (Le Tonnerre)"),
    (14, "Ibrahim (Abraham)"), (15, "Al-Hijr"), (16, "An-Nahl (Les Abeilles)"),
    (17, "Al-Isra (Le Voyage Nocturne)"), (18, "Al-Kahf (La Caverne)"), (19, "Maryam (Marie)"),
    (20, "Ta-Ha"), (21, "Al-Anbiya (Les Prophètes)"), (22, "Al-Hajj (Le Pèlerinage)"),
    (23, "Al-Mu'minun (Les Croyants)"), (24, "An-Nur (La Lumière)"), (25, "Al-Furqan (Le Discernement)"),
    (26, "Ash-Shu'ara (Les Poètes)"), (27, "An-Naml (Les Fourmis)"), (28, "Al-Qasas (Le Récit)"),
    (29, "Al-Ankabut (L'Araignée)"), (30, "Ar-Rum (Les Romains)"), (31, "Luqman"),
    (32, "As-Sajda (La Prosternation)"), (33, "Al-Ahzab (Les Coalisés)"), (34, "Saba"),
    (35, "Fatir (Le Créateur)"), (36, "Ya-Sin"), (37, "As-Saffat (Les Rangés)"),
    (38, "Sad"), (39, "Az-Zumar (Les Groupes)"), (40, "Ghafir (Le Pardonneur)"),
    (41, "Fussilat (Les Versets Détaillés)"), (42, "Ash-Shura (La Consultation)"), (43, "Az-Zukhruf (L'Ornement)"),
    (44, "Ad-Dukhan (La Fumée)"), (45, "Al-Jathiya (L'Agenouillée)"), (46, "Al-Ahqaf"),
    (47, "Muhammad"), (48, "Al-Fath (La Victoire)"), (49, "Al-Hujurat (Les Appartements)"),
    (50, "Qaf"), (51, "Adh-Dhariyat (Qui Éparpillent)"), (52, "At-Tur (Le Mont)"),
    (53, "An-Najm (L'Étoile)"), (54, "Al-Qamar (La Lune)"), (55, "Ar-Rahman (Le Tout Miséricordieux)"),
    (56, "Al-Waqi'a (L'Événement)"), (57, "Al-Hadid (Le Fer)"), (58, "Al-Mujadila (La Discussion)"),
    (59, "Al-Hashr (L'Exode)"), (60, "Al-Mumtahana (L'Éprouvée)"), (61, "As-Saff (Le Rang)"),
    (62, "Al-Jumu'a (Le Vendredi)"), (63, "Al-Munafiqun (Les Hypocrites)"), (64, "At-Taghabun (La Grande Perte)"),
    (65, "At-Talaq (Le Divorce)"), (66, "At-Tahrim (L'Interdiction)"), (67, "Al-Mulk (La Royauté)"),
    (68, "Al-Qalam (La Plume)"), (69, "Al-Haqqa (Celle qui Montre la Vérité)"), (70, "Al-Ma'arij (Les Voies d'Ascension)"),
    (71, "Nuh (Noé)"), (72, "Al-Jinn (Les Djinns)"), (73, "Al-Muzzammil (L'Enveloppé)"),
    (74, "Al-Muddaththir (Le Revêtu d'un Manteau)"), (75, "Al-Qiyama (La Résurrection)"), (76, "Al-Insan (L'Homme)"),
    (77, "Al-Mursalat (Les Envoyés)"), (78, "An-Naba (La Nouvelle)"), (79, "An-Nazi'at (Les Anges qui Arrachent)"),
    (80, "Abasa (Il s'est Renfrogné)"), (81, "At-Takwir (L'Obscurcissement)"), (82, "Al-Infitar (La Rupture)"),
    (83, "Al-Mutaffifin (Les Fraudeurs)"), (84, "Al-Inshiqaq (La Déchirure)"), (85, "Al-Buruj (Les Constellations)"),
    (86, "At-Tariq (L'Astre Nocturne)"), (87, "Al-A'la (Le Très-Haut)"), (88, "Al-Ghashiya (L'Enveloppante)"),
    (89, "Al-Fajr (L'Aube)"), (90, "Al-Balad (La Cité)"), (91, "Ash-Shams (Le Soleil)"),
    (92, "Al-Layl (La Nuit)"), (93, "Ad-Duha (Le Jour Montant)"), (94, "Ash-Sharh (L'Ouverture)"),
    (95, "At-Tin (Le Figuier)"), (96, "Al-Alaq (L'Adhérence)"), (97, "Al-Qadr (La Destinée)"),
    (98, "Al-Bayyina (La Preuve)"), (99, "Az-Zalzala (La Secousse)"), (100, "Al-Adiyat (Les Coursiers)"),
    (101, "Al-Qari'a (Le Fracas)"), (102, "At-Takathur (La Course aux Richesses)"), (103, "Al-Asr (Le Temps)"),
    (104, "Al-Humaza (Les Calomniateurs)"), (105, "Al-Fil (L'Éléphant)"), (106, "Quraysh"),
    (107, "Al-Ma'un (L'Ustensile)"), (108, "Al-Kawthar (L'Abondance)"), (109, "Al-Kafirun (Les Infidèles)"),
    (110, "An-Nasr (Les Secours)"), (111, "Al-Masad (Les Fibres)"), (112, "Al-Ikhlas (Le Monothéisme Pur)"),
    (113, "Al-Falaq (L'Aube Naissante)"), (114, "An-Nas (Les Hommes)"),
]


def import_quran_surahs():
    print("1/3 — Import des 114 Sourates du Coran (Cheikh Mishary Alafasy)...")
    existing = set(Son.objects.filter(categorie='CORAN').values_list('titre', flat=True))
    to_create = []
    for num, nom in SOURATES_114:
        titre = f"Sourate {num:03d} — {nom}"
        if titre in existing:
            continue
        url = f"https://server8.mp3quran.net/afs/{num:03d}.mp3"
        to_create.append(Son(
            titre=titre,
            auteur_voix="Cheikh Mishary Rashid Alafasy",
            categorie='CORAN',
            lien_audio_externe=url,
            est_premium=False,
        ))
    if to_create:
        Son.objects.bulk_create(to_create, batch_size=50)
    print(f"  => {len(to_create)} sourates ajoutées (Total CORAN : {Son.objects.filter(categorie='CORAN').count()})")


def import_xamxam_rss():
    print("2/3 — Import des enseignements Xam Xam (Podcloud / MediaMouride)...")
    try:
        resp = requests.get('https://khassida.lepodcast.fr/rss', timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"  [Erreur RSS] {e}")
        return

    root = ET.fromstring(resp.content)
    items = root.findall('./channel/item')
    ns = {'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}
    existing_titles = set(t.lower() for t in Son.objects.filter(categorie='XAM_XAM').values_list('titre', flat=True))

    to_create = []
    for it in items:
        t_el = it.find('title')
        enc = it.find('enclosure')
        if t_el is None or not t_el.text or enc is None:
            continue
        raw_title = re.sub(r'\s+', ' ', t_el.text.replace('_', ' ')).strip()
        audio_url = (enc.get('url') or '').strip()
        if not raw_title or not audio_url:
            continue
        if raw_title.lower() in existing_titles:
            continue
        existing_titles.add(raw_title.lower())

        author_el = it.find(f'{{{ns["itunes"]}}}author')
        author = author_el.text.strip() if (author_el is not None and author_el.text) else "Serigne Abdou Rahmane Mbacké"
        to_create.append(Son(
            titre=raw_title[:200],
            auteur_voix=author[:150],
            categorie='XAM_XAM',
            lien_audio_externe=audio_url,
            est_premium=False,
        ))

    if to_create:
        Son.objects.bulk_create(to_create, batch_size=50)
    print(f"  => {len(to_create)} cours Xam Xam ajoutés (Total XAM_XAM : {Son.objects.filter(categorie='XAM_XAM').count()})")


def upload_hybrid(file_path, titre, categorie):
    try:
        import cloudinary.uploader
        res = cloudinary.uploader.upload(
            file_path,
            resource_type='video',
            folder=f"media/audios/{categorie.lower()}",
            use_filename=True,
            unique_filename=True,
        )
        if res.get('secure_url'):
            return res['secure_url']
    except Exception as e:
        print(f"  [Cloudinary fallback local] {e}")

    ext = os.path.splitext(file_path)[1].lower() or '.mp3'
    local_dir = os.path.join(settings.BASE_DIR, 'static', 'audios_locaux', categorie.lower())
    os.makedirs(local_dir, exist_ok=True)
    safe_slug = re.sub(r'[^a-zA-Z0-9_\-]+', '_', titre)[:70] or 'audio'
    local_fname = f"{safe_slug}{ext}"
    shutil.copy2(file_path, os.path.join(local_dir, local_fname))
    return f"/static/audios_locaux/{categorie.lower()}/{local_fname}"


def import_missing_local_files():
    print("3/3 — Import des fichiers locaux manquants (Rajass, Adhan, Khassidas Kaolack & WKSM)...")
    base = settings.BASE_DIR
    candidates = [
        (os.path.join(base, 'media', 'audios', 'adhan', 'adhan.mp3'), "Adhan de Touba & La Mecque", "Muezzin", "ADHAN"),
        (os.path.join(base, 'sons', 'Bouchra_Lana_WKSM.mp3'), "Bouchra Lana — Wa Keur Serigne Massamba", "Wa Keur Serigne Massamba", "KHASSIDA"),
    ]
    # Ajouter Rajass
    for f in glob.glob(os.path.join(base, 'media', 'audios', 'rajass', '*.mp3')):
        clean_t = re.sub(r'[_\-]+', ' ', os.path.splitext(os.path.basename(f))[0]).strip()
        candidates.append((f, clean_t, "Serigne Abdoul Hakim Mbacké", "RAJASS"))
    # Ajouter Kaolack / J27 manquants dans media/audios/khassida/
    for pattern in ['*Kaolack*.mp3', '*J27_LAMYABDU*.mp3']:
        for f in glob.glob(os.path.join(base, 'media', 'audios', 'khassida', pattern)):
            if '(1)' in f or '(2)' in f:
                continue
            clean_t = re.sub(r'[_\-]+', ' ', os.path.splitext(os.path.basename(f))[0]).strip()
            candidates.append((f, clean_t, "Kurel 1 Kaolack HTDKH" if 'Kaolack' in f else "Kurel Wa Keur Serigne Massamba HT", "KHASSIDA"))

    added = 0
    for fpath, titre, auteur, cat in candidates:
        if not os.path.isfile(fpath):
            continue
        if Son.objects.filter(titre__iexact=titre).exists():
            continue
        print(f"  Upload [{cat}] : {titre}...")
        url = upload_hybrid(fpath, titre, cat)
        Son.objects.create(
            titre=titre[:200],
            auteur_voix=auteur[:150],
            categorie=cat,
            lien_audio_externe=url,
            est_premium=False,
        )
        added += 1

    # Ajouter Adhan Makkah vérifié si absent
    if not Son.objects.filter(titre__icontains="Makkah", categorie='ADHAN').exists():
        Son.objects.create(
            titre="Adhan de La Mecque (Masjid al-Haram)",
            auteur_voix="Al-Haram Makkah",
            categorie='ADHAN',
            lien_audio_externe="https://archive.org/download/MakkahAzan/Makkah-Azan.mp3",
            est_premium=False,
        )
        added += 1

    print(f"  => {added} audio(s) locaux / Adhan ajoutés.")


if __name__ == '__main__':
    import_quran_surahs()
    import_xamxam_rss()
    import_missing_local_files()
    from django.db.models import Count
    print("\n=== BILAN FINAL AUDIOTHÈQUE SDM ===")
    print("Total sons dans la base :", Son.objects.count())
    for row in Son.objects.values('categorie').annotate(c=Count('id')).order_by('-c'):
        print(f"  - {row['categorie']}: {row['c']}")
