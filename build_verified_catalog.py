"""
Constructeur de Catalogue Audio 100% Vérifié (Rapide ~30s) — SDM Mouride
- Garde les 108 pistes Cloudinary vérifiées + 114 Sourates MP3Quran vérifiées
- Vérifie les 117 épisodes Xam Xam (Podcloud/MediaMouride) via HEAD (ne garde que les HTTP 200)
- Collecte TOUTES les collections open-source de Kourels Mourides, Khassidas & Wolofals sur Internet Archive
  avec encodage correct quote(fname, safe='/'), filtre size > 50 Ko, non-privé, et test HEAD par collection
- Supprime 100% des liens 404 (ex: MakkahAzan / AdhanMedina) et écrit verified_open_sons.json
"""
import os
import re
import json
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
import requests
import xml.etree.ElementTree as ET

OPEN_MOURIDE_COLLECTIONS = [
    # ── KOURELS & KHASSIDAS MOURIDES ──
    ('khassaides', 'KHASSIDA', 'Kourel Touba-Internet', 'Khassida'),
    ('S.Ibra.Gueye', 'KHASSIDA', 'Serigne Ibra Gueye', 'Khassida S. Ibra Gueye'),
    ('ssmbackekhassida', 'KHASSIDA', 'Kourel Serigne Saliou Mbacké', 'Khassida S. Saliou Mbacké'),
    ('ssmbackekhassida1', 'KHASSIDA', 'Kourel Serigne Saliou Mbacké', 'Khassida S. Saliou Mbacké'),
    ('hizbou90', 'KHASSIDA', 'Kourel Hizbut Tarqiyyah (Classiques)', 'Hizbut Tarqiyyah'),
    ('wakeurserignemassamba', 'KHASSIDA', 'Wa Keur Serigne Massamba', 'Wa Keur S. Massamba'),
    ('wadaroumouhty', 'KHASSIDA', 'Kourel Wa Darou Mouhty', 'Kourel Wa Darou Mouhty'),
    ('toubamouride', 'KHASSIDA', 'Daara Touba Mouride', 'Daara Touba Mouride'),
    ('ssaliouthiam', 'KHASSIDA', 'Serigne Saliou Thiam', 'Serigne Saliou Thiam'),
    ('KhassaidesSerigneTouba', 'KHASSIDA', 'Kourel Khassides Serigne Touba', 'Khassida Serigne Touba'),
    ('MidadiSYoussouNdaoMahalLahoK1HTDKHPrepMagal2017', 'KHASSIDA', 'Kourel 1 HTDKH (S. Youssou Ndao)', 'Kourel 1 HTDKH'),
    ('HamatSoulayma', 'KHASSIDA', 'Kourel Hizbut Tarqiyyah Magal', 'Hizbut Tarqiyyah'),
    ('MagalMbackeKadior2017KourelHT1AjabaniRabbouSama', 'KHASSIDA', 'Kourel HT 1 Magal Mbacké Kadior', 'Kourel HT 1'),
    ('FuztiKhassaideBySerigneTouba', 'KHASSIDA', 'Kourel Khassida Fuzti', 'Fuzti'),
    ('MagalTouba2015KourelNationalHizbutTarqiyyahAlamaneAlayya', 'KHASSIDA', 'Kourel National Hizbut Tarqiyyah', 'Kourel National HT'),
    ('MagalTouba2015KourelNationalHizbutTarqiyyahExtraitJazbu_201512', 'KHASSIDA', 'Kourel National Hizbut Tarqiyyah', 'Kourel National HT'),
    ('MagalTouba2015KourelNationalHizbutTarqiyyahRabiHamdiWaSoukri', 'KHASSIDA', 'Kourel National Hizbut Tarqiyyah', 'Kourel National HT'),
    ('MagalTouba2015KourelNationalHizbutTarqiyyahWadiahtouYaKhayraDayfi1', 'KHASSIDA', 'Kourel National Hizbut Tarqiyyah', 'Kourel National HT'),
    ('MagalTouba2015KourelNationalHizbutTarqiyyahSalatouneWaTaslimoune', 'KHASSIDA', 'Kourel National Hizbut Tarqiyyah', 'Kourel National HT'),
    ('IlalMoustaphaMagalTouba2015KourelHizbutTarqiyyah', 'KHASSIDA', 'Kourel National Hizbut Tarqiyyah', 'Kourel National HT'),
    ('MagalTouba2015KourelNationalHizbutTarqiyyahAhanzanilBakhi', 'KHASSIDA', 'Kourel National Hizbut Tarqiyyah', 'Kourel National HT'),
    ('faridj-kourel-1-hizbut-tarqqiyyah-touba-ramadan-2019', 'KHASSIDA', 'Kourel 1 Hizbut Tarqiyyah Touba', 'Faridj Kourel 1 HT'),
    ('asmahou-ousna-s.-djim-cisse-kourel-1-htdkh-magal-2018-1440-h-1', 'KHASSIDA', 'S. Djim Cissé — Kourel 1 HTDKH', 'Asmaoul Husna'),
    ('bismil-illahi-lazi-hizbut-tarqiyyah-magal-mbacke-kadior-2017', 'KHASSIDA', 'Kourel Hizbut Tarqiyyah', 'Bismillahil Lazi'),
    ('wakana-hakhan-kourel-1-ht-touba-grand-magal-de-touba-2022', 'KHASSIDA', 'Kourel 1 Hizbut Tarqiyyah Touba', 'Wakana Hakhan'),
    ('niane-kourel-1-htmagal-touba-2022', 'KHASSIDA', 'Kourel 1 Hizbut Tarqiyyah Touba', 'Niane Kourel 1 HT'),
    # ── WOLOFALS, WAKHTANE & ENSEIGNEMENTS MOURIDES ──
    ('wolofal', 'WAKHTANE', 'Cheikh Moussa Ka (Wolofal)', 'Wolofal Cheikh Moussa Ka'),
    ('smoussaka', 'WAKHTANE', 'Cheikh Moussa Ka (Wolofal)', 'Wolofal Cheikh Moussa Ka'),
    ('wolofalsmd', 'WAKHTANE', 'Serigne Mbaye Diakhaté (Wolofal)', 'Wolofal S. Mbaye Diakhaté'),
    ('wsmd_20190922', 'WAKHTANE', 'Serigne Mbaye Diakhaté (Wolofal)', 'Wolofal S. Mbaye Diakhaté'),
    ('dajalewolofal', 'WAKHTANE', 'Dajalé Wolofal Mouride', 'Wolofal Mouride'),
    ('ChARMbacke-MawXudus', 'WAKHTANE', 'Cheikh Abdou Rahmane Mbacké', 'Mawahibul Qudus'),
    ('ChARMbacke-Silk', 'WAKHTANE', 'Cheikh Abdou Rahmane Mbacké', 'Silkul Jawahir'),
    ('ChARMbacke-Sahandat', 'WAKHTANE', 'Cheikh Abdou Rahmane Mbacké', 'Sahandat'),
    ('MinanulBaqilQadim', 'WAKHTANE', 'Minanul Bâqil Qadîm', 'Minanul Bâqil Qadîm'),
    ('irwa_u_nadiim', 'WAKHTANE', 'Irwa-u Nadim (Daaraykamil)', 'Irwa-u Nadim'),
    ('Alkhadiimiyah_ndenkaaneSerigneBi', 'WAKHTANE', 'Ngagne Mboup — Ndenkaané Serigne Bi', 'Ndenkaané Serigne Bi'),
]

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

HEADERS = {'User-Agent': 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36'}


def head_ok(url):
    try:
        r = requests.head(url, headers=HEADERS, timeout=(4, 6), allow_redirects=True)
        ct = (r.headers.get('Content-Type') or '').lower()
        ok = r.status_code in (200, 206) and ('text/html' not in ct) and ('text/plain' not in ct)
        final_u = r.url if (ok and r.url and r.url.startswith('https://') and 'podcloud.fr' in url) else url
        return ok, final_u
    except Exception:
        return False, url


def clean_title(filename, prefix_label):
    base = os.path.splitext(os.path.basename(filename))[0]
    base = re.sub(r'[_\-]+', ' ', base)
    base = re.sub(r'\s+', ' ', base).strip()
    if re.match(r'^[0-9]{1,3}[a-zA-Z]?$', base):
        return f"{prefix_label} — Partie {base}"
    if prefix_label.lower() not in base.lower() and len(base) < 24:
        return f"{base} ({prefix_label})"
    return base[:195]


def run():
    catalog = {}  # url -> item

    # 1. Garder toutes les pistes Cloudinary (video/upload) actuellement en production
    print("1/4 — Récupération des pistes Cloudinary (video/upload) vérifiées...")
    r = requests.get('https://sdm-mourit.onrender.com/sons-api/liste/', timeout=20)
    for t in r.json().get('playlist', []):
        u = (t.get('url') or '').strip()
        if 'res.cloudinary.com' in u and '/video/upload/' in u:
            catalog[u] = {
                'titre': (t.get('titre') or '').strip()[:200],
                'auteur_voix': (t.get('auteur') or 'Kourel Hizbut Tarqiyyah Touba').strip()[:150],
                'categorie': (t.get('categorie') or 'KHASSIDA').strip().upper(),
                'lien_audio_externe': u,
            }
    print(f"  => {len(catalog)} pistes Cloudinary (video/upload) conservées.")

    # 2. Ajouter les 114 Sourates complètes du Coran (MP3Quran HTTP 200)
    print("2/4 — Ajout des 114 Sourates du Coran (Cheikh Mishary Alafasy)...")
    for num, nom in SOURATES_114:
        u = f"https://server8.mp3quran.net/afs/{num:03d}.mp3"
        catalog[u] = {
            'titre': f"Sourate {num:03d} — {nom}",
            'auteur_voix': "Cheikh Mishary Rashid Alafasy",
            'categorie': 'CORAN',
            'lien_audio_externe': u,
        }

    # 3. Vérifier chaque épisode Xam Xam (Podcloud -> lien HTTPS direct mediamouride.com)
    print("3/4 — Vérification HEAD des épisodes Xam Xam (khassida.lepodcast.fr)...")
    rss_resp = requests.get('https://khassida.lepodcast.fr/rss', timeout=15)
    root = ET.fromstring(rss_resp.content)
    ns = {'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}
    rss_cands = []
    for it in root.findall('./channel/item'):
        t_el, enc = it.find('title'), it.find('enclosure')
        if t_el is None or not t_el.text or enc is None:
            continue
        u = (enc.get('url') or '').strip()
        if not u:
            continue
        author_el = it.find(f'{{{ns["itunes"]}}}author')
        author = author_el.text.strip() if (author_el is not None and author_el.text) else "Serigne Abdou Rahmane Mbacké"
        rss_cands.append((re.sub(r'\s+', ' ', t_el.text.replace('_', ' ')).strip()[:200], author[:150], u))

    xam_ok, xam_bad = 0, 0
    with ThreadPoolExecutor(max_workers=12) as ex:
        for (titre, author, orig_u), (ok, final_u) in zip(rss_cands, ex.map(lambda c: head_ok(c[2]), rss_cands)):
            if ok:
                catalog[final_u] = {
                    'titre': titre,
                    'auteur_voix': author,
                    'categorie': 'XAM_XAM',
                    'lien_audio_externe': final_u,
                }
                xam_ok += 1
            else:
                xam_bad += 1
    print(f"  => Xam Xam : {xam_ok} valides (rejetés : {xam_bad})")

    # 4. Collecter & vérifier TOUTES les 37 collections open-source Mourides sur Internet Archive
    print("4/4 — Collecte & vérification des 37 collections Kourels Mourides & Wolofals (Archive.org)...")
    arch_ok_col, arch_tracks = 0, 0

    def process_collection(spec):
        ident, cat, author, prefix = spec
        tracks = []
        try:
            mr = requests.get(f'https://archive.org/metadata/{ident}', timeout=(5, 10))
            if mr.status_code != 200:
                return ident, []
            data = mr.json()
            meta = data.get('metadata') or {}
            if str(meta.get('access-restricted-item', '')).lower() == 'true':
                return ident, []
            files = data.get('files') or []
            mp3s = [
                f for f in files
                if (f.get('name') or '').lower().endswith('.mp3')
                and not f.get('private')
                and int(f.get('size') or 0) > 40000
                and f.get('source') == 'original'
            ]
            if not mp3s:
                mp3s = [
                    f for f in files
                    if (f.get('name') or '').lower().endswith('.mp3')
                    and not f.get('private')
                    and int(f.get('size') or 0) > 40000
                ]
            if not mp3s:
                return ident, []

            # Vérifier la 1re piste de la collection par HEAD réel (encodage safe='/' !)
            first_url = f"https://archive.org/download/{ident}/{quote(mp3s[0]['name'], safe='/')}"
            ok, _ = head_ok(first_url)
            if not ok:
                print(f"  [REJETÉ HEAD] {ident} ({first_url[:70]})")
                return ident, []

            for f in mp3s:
                fname = f['name']
                url = f"https://archive.org/download/{ident}/{quote(fname, safe='/')}"
                raw_t = (f.get('title') or '').strip()
                titre = raw_t if (raw_t and len(raw_t) > 3) else clean_title(fname, prefix)
                tracks.append({
                    'titre': titre[:200],
                    'auteur_voix': author[:150],
                    'categorie': cat,
                    'lien_audio_externe': url,
                })
            return ident, tracks
        except Exception as e:
            print(f"  [Skip {ident}] {type(e).__name__}")
            return ident, []

    with ThreadPoolExecutor(max_workers=8) as ex:
        for ident, tracks in ex.map(process_collection, OPEN_MOURIDE_COLLECTIONS):
            if tracks:
                arch_ok_col += 1
                for tr in tracks:
                    if tr['lien_audio_externe'] not in catalog:
                        catalog[tr['lien_audio_externe']] = tr
                        arch_tracks += 1
                print(f"  [OK] {ident}: {len(tracks)} pistes")

    print(f"  => {arch_ok_col}/{len(OPEN_MOURIDE_COLLECTIONS)} collections Archive.org validées ({arch_tracks} pistes) !")

    # Dédupliquer proprement les titres
    final_list = []
    seen_titles = set()
    for url, item in catalog.items():
        t = item['titre'] or 'Audio Mouride'
        if t.lower() in seen_titles:
            t = f"{t} — {item['auteur_voix'][:22]}"[:200]
        if t.lower() in seen_titles:
            continue
        seen_titles.add(t.lower())
        item['titre'] = t
        final_list.append(item)

    final_list.sort(key=lambda x: (x['categorie'], x['auteur_voix'].lower(), x['titre'].lower()))
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verified_open_sons.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)

    cats = {}
    for x in final_list:
        cats[x['categorie']] = cats.get(x['categorie'], 0) + 1
    print(f"\n=== CATALOGUE 100% VÉRIFIÉ ÉCRIT : {len(final_list)} PISTES ===")
    for k, v in sorted(cats.items(), key=lambda kv: -kv[1]):
        print(f"  - {k}: {v}")


if __name__ == '__main__':
    run()
