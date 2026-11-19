"""
Script idempotent exécuté en local ET automatiquement lors du build Render (build.sh) :
0. Standardise les 30 Jukkis du Saint Coran (numero=1..30, titre="Jukki X (Juz X)") et nettoie les doublons/vides
1. Ajoute les 114 Sourates complètes du Coran Audio (Cheikh Mishary Alafasy — HTTP 200)
2. Ajoute les 117 Enseignements Xam Xam (Tasawudu Sighaar, Tasawudu Chuban, Masaalikul Jinaan, Rissaala...)
3. Ajoute ~257 Audios Mourides open-access depuis Internet Archive (Khassidas, Kourels, Serigne Ibra Gueye,
   Kourel Serigne Saliou Mbacké, Hizbut Tarqiyyah, Wolofal Serigne Mbaye Diakhaté, Cheikh Abdou Rahmane Mbacké,
   Minanul Bâqil Qadîm, Irwa-u Nadim, Ndenkaané Serigne Bi)
4. Ajoute les Adhans et fichiers locaux manquants (Rajass, Bouchra Lana, Kaolack...)
"""
import os
import re
import glob
import shutil
from urllib.parse import quote
import requests
import xml.etree.ElementTree as ET
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from django.conf import settings
from django.db.models import Count
from bibliotheque.models import Son, Coran

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

ARCHIVE_MOURIDE_COLLECTIONS = [
    ('khassaides', 'KHASSIDA', 'Kourel Touba-Internet', 'Khassida'),
    ('S.Ibra.Gueye', 'KHASSIDA', 'Serigne Ibra Gueye', 'Khassida S. Ibra Gueye'),
    ('ssmbackekhassida', 'KHASSIDA', 'Kourel Serigne Saliou Mbacké', 'Khassida S. Saliou Mbacké'),
    ('hizbou90', 'KHASSIDA', 'Kourel Hizbut Tarqiyyah (Classiques)', 'Hizbut Tarqiyyah'),
    ('wolofalsmd', 'WAKHTANE', 'Serigne Mbaye Diakhaté (Wolofal)', 'Wolofal'),
    ('ChARMbacke-MawXudus', 'WAKHTANE', 'Cheikh Abdou Rahmane Mbacké', 'Mawahibul Qudus'),
    ('MinanulBaqilQadim', 'WAKHTANE', 'Minanul Bâqil Qadîm', 'Minanul Bâqil Qadîm'),
    ('irwa_u_nadiim', 'WAKHTANE', 'Irwa-u Nadim (Daaraykamil)', 'Irwa-u Nadim'),
    ('Alkhadiimiyah_ndenkaaneSerigneBi', 'WAKHTANE', 'Ngagne Mboup — Ndenkaané Serigne Bi', 'Ndenkaané Serigne Bi'),
]


def standardize_coran_jukkis():
    print("0/4 — Standardisation des 30 Jukkis du Saint Coran...")
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


def import_quran_surahs():
    print("1/4 — Import des 114 Sourates du Coran (Cheikh Mishary Alafasy)...")
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
        Son.objects.bulk_create(to_create, batch_size=60)
    print(f"  => {len(to_create)} sourates ajoutées (Total CORAN : {Son.objects.filter(categorie='CORAN').count()})")


def import_xamxam_rss():
    print("2/4 — Import des 117 enseignements Xam Xam (Podcloud / MediaMouride)...")
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
        if not raw_title or not audio_url or raw_title.lower() in existing_titles:
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
        Son.objects.bulk_create(to_create, batch_size=60)
    print(f"  => {len(to_create)} cours Xam Xam ajoutés (Total XAM_XAM : {Son.objects.filter(categorie='XAM_XAM').count()})")


def clean_archive_track_title(filename, prefix_label):
    base = os.path.splitext(os.path.basename(filename))[0]
    base = re.sub(r'[_\-]+', ' ', base)
    base = re.sub(r'\s+', ' ', base).strip()
    # Si le nom du fichier n'est qu'un numéro ("01A", "22", "1"), ajouter le préfixe lisible de la collection
    if re.match(r'^[0-9]{1,3}[a-zA-Z]?$', base):
        return f"{prefix_label} — Partie {base}"
    if prefix_label.lower() not in base.lower() and len(base) < 28:
        return f"{base} ({prefix_label})"
    return base[:195]


def import_archive_org_mouride():
    print("3/4 — Import des archives Mourides open-access (Internet Archive)...")
    existing_urls = set(Son.objects.exclude(lien_audio_externe='').values_list('lien_audio_externe', flat=True))
    existing_titles = set(t.lower() for t in Son.objects.values_list('titre', flat=True))
    to_create = []

    for ident, cat, default_author, prefix_lbl in ARCHIVE_MOURIDE_COLLECTIONS:
        try:
            r = requests.get(f'https://archive.org/metadata/{ident}/files', timeout=12)
            if r.status_code != 200:
                continue
            files = r.json().get('result', [])
            mp3s = [f for f in files if (f.get('name') or '').lower().endswith('.mp3') and f.get('source') == 'original']
            if not mp3s:
                mp3s = [f for f in files if (f.get('name') or '').lower().endswith('.mp3')]

            for f in mp3s:
                fname = f.get('name') or ''
                if not fname:
                    continue
                url = f"https://archive.org/download/{ident}/{quote(fname)}"
                if url in existing_urls:
                    continue

                raw_meta_title = (f.get('title') or '').strip()
                titre = raw_meta_title if (raw_meta_title and len(raw_meta_title) > 3) else clean_archive_track_title(fname, prefix_lbl)
                if titre.lower() in existing_titles:
                    titre = f"{titre} ({ident[:8]})"[:200]

                existing_urls.add(url)
                existing_titles.add(titre.lower())
                to_create.append(Son(
                    titre=titre[:200],
                    auteur_voix=default_author[:150],
                    categorie=cat,
                    lien_audio_externe=url,
                    est_premium=False,
                ))
        except Exception as e:
            print(f"  [Skip {ident}] {e}")

    if to_create:
        Son.objects.bulk_create(to_create, batch_size=80)
    print(f"  => {len(to_create)} audio(s) Mourides Archive.org ajoutés.")


def import_adhan_and_local():
    print("4/4 — Vérification Adhan & fichiers locaux complémentaires...")
    added = 0
    if not Son.objects.filter(titre__icontains="Makkah", categorie='ADHAN').exists():
        Son.objects.create(
            titre="Adhan de La Mecque (Masjid al-Haram)",
            auteur_voix="Al-Haram Makkah",
            categorie='ADHAN',
            lien_audio_externe="https://archive.org/download/MakkahAzan/Makkah-Azan.mp3",
            est_premium=False,
        )
        added += 1
    if not Son.objects.filter(titre__icontains="Médine", categorie='ADHAN').exists():
        Son.objects.create(
            titre="Adhan de Médine (Al-Masjid an-Nabawi)",
            auteur_voix="Al-Masjid an-Nabawi",
            categorie='ADHAN',
            lien_audio_externe="https://archive.org/download/AdhanMedina/Adhan-Medina.mp3",
            est_premium=False,
        )
        added += 1
    print(f"  => {added} Adhan(s) ajoutés.")


if __name__ == '__main__':
    standardize_coran_jukkis()
    import_quran_surahs()
    import_xamxam_rss()
    import_archive_org_mouride()
    import_adhan_and_local()
    print("\n=== BILAN FINAL AUDIOTHÈQUE SDM ===")
    print("Total sons dans la base :", Son.objects.count())
    for row in Son.objects.values('categorie').annotate(c=Count('id')).order_by('-c'):
        print(f"  - {row['categorie']}: {row['c']}")
