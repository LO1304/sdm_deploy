import os
import datetime
import requests
import json
import hashlib
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum, Count
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

from django.utils.timezone import now
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token

# Import de tes modèles
from django.core.management import call_command
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.conf import settings

def trigger_daily_tasks(request):
    token = request.GET.get('token')
    # On utilise SECRET_KEY comme token de sécurité (les 20 premiers caractères)
    expected_token = settings.SECRET_KEY[:20]
    
    if token != expected_token:
        return HttpResponse("Non autorisé", status=403)
        
    try:
        call_command('run_daily_tasks')
        return JsonResponse({"status": "success", "message": "Tâches quotidiennes exécutées avec succès."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

from .models import (
    Khassida, Coran, Zikr, Wird, EtapeWird, HistoriqueWird, ProgressionWird, Son, Profile, HistoriqueConsultation, Favori, Telechargement, ContenuDuJour, ParametresPriere, ProgressionLecture, Historique, HistoriqueZikr, ProgressionGenerale,
    SessionZikrCommunautaire, ParticipationZikrCommunautaire, Notification,
    SessionKaamil, JukkiKaamil
)
from .forms import ModernRegisterForm


# --- HELPER : VÉRIFICATION PREMIUM ---

def _user_is_premium(user):
    """Vérifie si un utilisateur est Premium."""
    if not user.is_authenticated:
        return False
    try:
        return user.profile.est_premium
    except Profile.DoesNotExist:
        return False


def _check_premium_access(request, content_obj):
    """Vérifie l'accès premium et retourne une redirection si bloqué, sinon None."""
    if getattr(content_obj, 'est_premium', False) and not _user_is_premium(request.user):
        return render(request, 'bibliotheque/premium_required.html', {
            'contenu_titre': getattr(content_obj, 'titre', 'Contenu Premium'),
        })
    return None


# --- HELPER : DOSSIERS EXISTANTS & PROFILS DE KOURELS / MAÎTRES ---

AUDIO_FOLDER_META = {
    'KHASSIDA': {
        'label': 'Khassidas & Kourels',
        'subtitle': 'Kourels Hizbut Tarqiyyah, Touba & Maîtres',
        'icon': 'fa-feather-pointed',
        'gradient': 'linear-gradient(135deg, #D4AF37, #78350F)',
        'order': 1,
    },
    'WAKHTANE': {
        'label': 'Wakhtane & Wolofals',
        'subtitle': 'Wolofals sacrés, récits & enseignements',
        'icon': 'fa-microphone-lines',
        'gradient': 'linear-gradient(135deg, #F59E0B, #9A3412)',
        'order': 2,
    },
    'XAM_XAM': {
        'label': 'Xam Xam & Daara',
        'subtitle': 'Sciences religieuses & explications',
        'icon': 'fa-graduation-cap',
        'gradient': 'linear-gradient(135deg, #38BDF8, #1E3A8A)',
        'order': 3,
    },
    'CORAN': {
        'label': 'Saint Coran (Audio)',
        'subtitle': 'Les 114 Sourates complètes',
        'icon': 'fa-book-quran',
        'gradient': 'linear-gradient(135deg, #10B981, #064E3B)',
        'order': 4,
    },
    'ZIKR': {
        'label': 'Zikr & Invocations',
        'subtitle': 'Litanies et pratiques spirituelles',
        'icon': 'fa-hands-praying',
        'gradient': 'linear-gradient(135deg, #A855F7, #4C1D95)',
        'order': 5,
    },
    'RAJASS': {
        'label': 'Rajass & Chants',
        'subtitle': 'Chants mourides traditionnels',
        'icon': 'fa-music',
        'gradient': 'linear-gradient(135deg, #F43F5E, #881337)',
        'order': 6,
    },
    'BASSIROU_KHELCOM': {
        'label': 'Serigne Bassirou Mbacké Khelcom',
        'subtitle': 'Wakhtanes, Khassidas & Enseignements intégraux',
        'icon': 'fa-microphone-lines',
        'gradient': 'linear-gradient(135deg, #F59E0B, #065F46)',
        'order': 2,
    },
    'ADHAN': {
        'label': 'Adhan & Appels',
        'subtitle': 'Appels à la prière',
        'icon': 'fa-mosque',
        'gradient': 'linear-gradient(135deg, #14B8A6, #134E4A)',
        'order': 8,
    },
}

PROFILE_PALETTES = [
    'linear-gradient(135deg, #D4AF37, #78350F)',
    'linear-gradient(135deg, #10B981, #064E3B)',
    'linear-gradient(135deg, #38BDF8, #1E3A8A)',
    'linear-gradient(135deg, #F59E0B, #9A3412)',
    'linear-gradient(135deg, #A855F7, #4C1D95)',
    'linear-gradient(135deg, #F43F5E, #881337)',
    'linear-gradient(135deg, #14B8A6, #134E4A)',
]


PROFILE_IMAGES = [
    '/static/images/audio_thumbs/touba.jpg',
    '/static/images/audio_thumbs/khassida.jpg',
    '/static/images/audio_thumbs/mosquee.jpg',
    '/static/images/audio_thumbs/auth_or.jpg',
    '/static/images/audio_thumbs/medine.jpg',
    '/static/images/audio_thumbs/kaaba.jpg',
    '/static/images/audio_thumbs/parchemin.jpg',
    '/static/images/audio_thumbs/firdaws.jpg',
    '/static/images/audio_thumbs/aurore.jpg',
    '/static/images/audio_thumbs/pattern.jpg',
]

FOLDER_IMAGES = {
    'KHASSIDA': '/static/images/audio_thumbs/touba.jpg',
    'BASSIROU_KHELCOM': '/static/images/audio_thumbs/serigne_touba.jpg',
    'WAKHTANE': '/static/images/audio_thumbs/serigne_touba.jpg',
    'XAM_XAM': '/static/images/audio_thumbs/parchemin.jpg',
    'CORAN': '/static/images/audio_thumbs/kaaba.jpg',
    'ZIKR': '/static/images/audio_thumbs/medine.jpg',
    'RAJASS': '/static/images/audio_thumbs/aurore.jpg',
    'ADHAN': '/static/images/audio_thumbs/mosquee.jpg',
}


def _pick_profile_image(name, cat):
    low = (name or '').lower()
    if any(k in low for k in ('bamba', 'touba', 'bassirou', 'saliou', 'abdou', 'mback')):
        return '/static/images/audio_thumbs/touba.jpg'
    if any(k in low for k in ('ahlu', 'khadim', 'hizbut', 'kourel', 'kurel', 'khassida')):
        return '/static/images/audio_thumbs/khassida.jpg'
    if cat == 'CORAN':
        return '/static/images/audio_thumbs/kaaba.jpg'
    if cat == 'XAM_XAM':
        return '/static/images/audio_thumbs/parchemin.jpg'
    return PROFILE_IMAGES[sum(ord(c) for c in (name or 'SDM')) % len(PROFILE_IMAGES)]


def _is_bassirou_khelcom_author(auteur_voix):
    low = (auteur_voix or '').lower()
    return ('bassirou' in low) and ('mback' in low or 'khelcom' in low)


def _build_audio_folders_and_profiles(queryset):
    """
    Regroupe les profils existants (Kourels, Maîtres, Récitants) directement à l'intérieur
    de leurs dossiers/catégories existants (Khassidas, Serigne Bassirou Mbacké Khelcom, Wakhtane, Xam Xam, Coran, etc.)
    avec une image nette existante par dossier et par profil.
    """
    cat_labels = dict(Son.CATEGORIES)
    folder_map = {}
    flat_profiles = {}

    rows = queryset.values('categorie', 'auteur_voix').annotate(total=Count('id')).order_by('-total')
    for row in rows:
        raw_name = (row['auteur_voix'] or '').strip()
        if _is_bassirou_khelcom_author(raw_name):
            cat = 'BASSIROU_KHELCOM'
            name = 'Serigne Bassirou Mbacké Khelcom'
        else:
            cat = (row['categorie'] or 'KHASSIDA').upper()
            name = raw_name or cat_labels.get(cat, 'Collection SDM')
        words = [w for w in name.replace('—', ' ').replace('-', ' ').split() if w]
        initials = (words[0][0] + (words[1][0] if len(words) > 1 else '')).upper() if words else 'SD'
        gradient = PROFILE_PALETTES[sum(ord(c) for c in name) % len(PROFILE_PALETTES)]
        p_image = _pick_profile_image(name, cat)

        if cat not in folder_map:
            meta = AUDIO_FOLDER_META.get(cat, {
                'label': cat_labels.get(cat, cat),
                'subtitle': 'Collection audio',
                'icon': 'fa-folder',
                'gradient': 'linear-gradient(135deg, #D4AF37, #065F46)',
                'order': 99,
            })
            folder_map[cat] = {
                'code': cat,
                'label': meta['label'],
                'subtitle': meta['subtitle'],
                'icon': meta['icon'],
                'gradient': meta['gradient'],
                'image': FOLDER_IMAGES.get(cat, '/static/images/audio_thumbs/touba.jpg'),
                'order': meta['order'],
                'total_tracks': 0,
                'profiles_dict': {},
            }

        f_entry = folder_map[cat]
        f_entry['total_tracks'] += row['total']
        pkey = name.lower()
        if pkey not in f_entry['profiles_dict']:
            f_entry['profiles_dict'][pkey] = {
                'nom': name,
                'initials': initials,
                'categorie': cat,
                'categorie_label': f_entry['label'],
                'count': 0,
                'gradient': gradient,
                'image': p_image,
            }
        f_entry['profiles_dict'][pkey]['count'] += row['total']

        # Profil à plat (pour recherche / banner profil actif)
        if pkey not in flat_profiles:
            flat_profiles[pkey] = {
                'nom': name,
                'initials': initials,
                'categorie': cat,
                'categorie_label': f_entry['label'],
                'count': 0,
                'gradient': gradient,
                'image': p_image,
            }
        flat_profiles[pkey]['count'] += row['total']

    folders_tree = []
    for f in sorted(folder_map.values(), key=lambda x: (x['order'], -x['total_tracks'])):
        profs = sorted(f['profiles_dict'].values(), key=lambda x: (-x['count'], x['nom']))
        folders_tree.append({
            'code': f['code'],
            'label': f['label'],
            'subtitle': f['subtitle'],
            'icon': f['icon'],
            'gradient': f['gradient'],
            'image': f['image'],
            'total_tracks': f['total_tracks'],
            'total_profiles': len(profs),
            'profiles': profs,
            'preview_profiles': profs[:4],
        })

    collections_profiles = sorted(flat_profiles.values(), key=lambda x: (-x['count'], x['nom']))
    return folders_tree, collections_profiles, flat_profiles


# --- HELPER : DOSSIERS PAR TITRE D'ŒUVRE AVEC IMAGES EXISTANTES ---

TITLE_FOLDER_RULES = [
    ('mawahibou-nafih', 'Mawahibou Nâfih', ['mawahib', 'mawaahib'], 'khassida.png'),
    ('jazbul-qulub', 'Jazbul Qulûb', ['jazbu', 'jazbo', 'jusbu', 'djazbu'], 'mosque_touba.png'),
    ('midaadi', 'Midaadi Wa Aqlâmî', ['midad', 'midaad'], 'mouride.jpg'),
    ('farij', 'Farij (Ramadan)', ['farij', 'farji'], 'mosquee.jpg'),
    ('lam-yabdu', 'Lam Yabdu', ['lamyabd', 'lam yabd'], 'islamic_pattern.png'),
    ('matlabul-fawzayni', 'Matlabul Fawzayni & Chifâ\'', ['matlabu', 'matlabo'], 'mosque_touba.png'),
    ('sindidi', 'Sindidi', ['sindid'], 'khassida.png'),
    ('huqqal-bukau', 'Huqqal Bukâ\'u', ['huqqa', 'houqqa'], 'mouride.jpg'),
    ('jaalibatul-marakhib', 'Jaalibatul Marakhib', ['jaalibat', 'jalibat', 'dialibat', 'djalibat'], 'mosque_touba.png'),
    ('chahru-ramadan', 'Chahru Ramadan', ['chahru ramadan', 'bichahri', 'shahru ramadan'], 'mosquee.jpg'),
    ('ya-khayra', 'Yâ Khayra Dayfin', ['yakhayra', 'ya khayra'], 'islamic_pattern.png'),
    ('asmaul-husna', 'Asma\'ul Husna', ['asmaoul', 'asmaul', 'asmaa'], 'auth_bg.png'),
    ('bismillahil-lazi', 'Bismillâhil Lazî', ['bismilah', 'bismillah'], 'khassida.png'),
    ('ajabani', 'Ajabanî Rabbou Samâ', ['ajabani', 'adjabani'], 'mosque_touba.png'),
    ('ahbabtu', 'Ahbabtu', ['ahbabtu'], 'mouride.jpg'),
    ('taysirul-assir', 'Taysîrul Assîr', ['taysir'], 'mosquee.jpg'),
    ('tawbatun-nasuh', 'Tawbatun Nasûh', ['tawbat'], 'islamic_pattern.png'),
    ('wakana-haqqan', 'Wakâna Haqqan', ['wakana', 'wakaana'], 'mosque_touba.png'),
    ('muqaddimatul-amdah', 'Muqaddimâtul Amdâh', ['moukhadimat', 'muqaddimat', 'mouxadimat', 'mukhadimat'], 'khassida.png'),
    ('mimiya', 'Mîmiya', ['mimiya', 'miimiya'], 'mouride.jpg'),
    ('minanul-baqil-qadim', 'Minanul Bâqil Qadîm', ['minan'], 'mosquee.jpg'),
    ('irwaun-nadim', 'Irwâ\'un Nadîm', ['irwa', 'irwaa'], 'islamic_pattern.png'),
    ('buchra-lana', 'Buchrâ Lanâ', ['buchra', 'bouchra'], 'mosque_touba.png'),
    ('madal-khabiru', 'Madal Khabîru & Lissânu Chukr', ['madal', 'lissanu', 'lissanou'], 'khassida.png'),
    ('astaghfirullaha-bihi', 'Astaghfirullâha Bihi', ['astahfir', 'astaghfir'], 'mouride.jpg'),
    ('ya-mukrima', 'Yâ Mukrima Dayf', ['yaamoukrima', 'yamukrima', 'ya mukrima'], 'mosquee.jpg'),
    ('walaqad-karamna', 'Walaqad Karamna', ['walaqad', 'walakhad'], 'islamic_pattern.png'),
    ('tazawwudu-cighar', 'Tazawwudu-ç-Çighâr', ['tasawud', 'tazawwud', 'tazawud'], 'mosque_touba.png'),
    ('nahju-qadail-haj', 'Nahju Qadâ\'il Hâj', ['nahju', 'nahjou'], 'khassida.png'),
    ('fuzti', 'Fuzti / Fuztu', ['fuzti', 'fuztu', 'fouzti'], 'mouride.jpg'),
    ('ila-nabiyyin', 'Ilâ Nabiyyin', ['ilaanabiyin', 'ilaa nabiyin', 'ila nabiy'], 'mosquee.jpg'),
    ('ala-innani', 'Alâ Innanî', ['alaa inani', 'ala inani', 'ala innani'], 'islamic_pattern.png'),
    ('wolofal-mouride', 'Wolofal Mouride', ['wolofal', 'wsmd', 'smdikhate', 'dajale'], 'mouride.jpg'),
    ('sourates-coran', 'Sourates du Saint Coran', ['sourate', 'surah'], 'mosquee.jpg'),
    ('xam-xam-cours', 'Xam Xam & Enseignements', ['xam xam', 'tafsir', 'imamul', 'hazali', 'ghazali', 'jeunesse', 'jataay', 'ndiguel'], 'auth_bg.png'),
]

EXISTING_FALLBACK_IMAGES = [
    '/static/images/mosque_touba.png',
    '/static/images/khassida.png',
    '/static/images/mouride.jpg',
    '/static/images/mosquee.jpg',
    '/static/images/islamic_pattern.png',
    '/static/images/auth_bg.png',
]


def _classify_title_folder(titre, categorie):
    low = (titre or '').lower()
    for slug, label, keywords, img_name in TITLE_FOLDER_RULES:
        if any(k in low for k in keywords):
            return slug, label, f'/static/images/{img_name}'
    if categorie == 'CORAN':
        return 'sourates-coran', 'Sourates du Saint Coran', '/static/images/mosquee.jpg'
    if categorie == 'WAKHTANE':
        return 'wolofal-mouride', 'Wolofal & Wakhtane', '/static/images/mouride.jpg'
    if categorie == 'XAM_XAM':
        return 'xam-xam-cours', 'Xam Xam & Enseignements', '/static/images/auth_bg.png'
    return 'autres-khassidas', 'Autres Khassidas & Œuvres', '/static/images/khassida.png'


def _build_audio_title_folders(sons_list):
    """
    Regroupe les sons par Dossier Titre d'Œuvre (Mawahibou, Jazbul Qulub, Midaadi, Farij, etc.)
    en associant automatiquement les images existantes (miniatures Khassidas PDF ou images static/images).
    """
    # Index rapide des Khassidas PDF existants pour réutiliser leurs vraies images/couvertures
    khassida_thumbs = []
    try:
        for kh in Khassida.objects.only('id', 'titre', 'image_couverture'):
            t_low = (kh.titre or '').lower()
            img_url = kh.image_couverture.url if kh.image_couverture else f'/thumb-pdf/khassida/{kh.id}/'
            khassida_thumbs.append((t_low, img_url))
    except Exception:
        pass

    buckets = {}
    son_to_slug = {}
    for s in sons_list:
        slug, label, fallback_img = _classify_title_folder(s.titre, s.categorie)
        son_to_slug[s.id] = slug
        if slug not in buckets:
            # Chercher une miniature de 1re page / couverture Khassida existante correspondante
            thumb_img = fallback_img
            matched_keywords = next((kws for sl, _, kws, _ in TITLE_FOLDER_RULES if sl == slug), [])
            if matched_keywords and slug not in ('sourates-coran', 'wolofal-mouride', 'xam-xam-cours', 'farij'):
                for kh_low, kh_img in khassida_thumbs:
                    if any(k in kh_low for k in matched_keywords):
                        thumb_img = kh_img
                        break
            buckets[slug] = {
                'slug': slug,
                'titre': label,
                'image': thumb_img,
                'fallback_image': fallback_img,
                'count': 0,
                'profiles': set(),
            }
        buckets[slug]['count'] += 1
        if s.auteur_voix:
            buckets[slug]['profiles'].add(s.auteur_voix)

    title_folders = []
    for b in sorted(buckets.values(), key=lambda x: (-x['count'], x['titre'])):
        title_folders.append({
            'slug': b['slug'],
            'titre': b['titre'],
            'image': b['image'],
            'fallback_image': b['fallback_image'],
            'count': b['count'],
            'profiles_count': len(b['profiles']),
        })
    return title_folders, son_to_slug


def _invalidate_catalog_cache():
    cache.delete_many([
        'sdm_audio_catalog_v3',
        f'sdm_home_public_v1_{datetime.date.today().isoformat()}',
    ])


def _get_cached_audio_catalog():
    """Construit et met en cache en mémoire le catalogue audio complet (dossiers, profils, titres, pistes compactes)."""
    cached = cache.get('sdm_audio_catalog_v3')
    if cached is not None:
        return cached

    cat_labels = dict(Son.CATEGORIES)
    all_qs = Son.objects.all().order_by('-date_ajout', 'titre')
    folders_tree, collections_profiles, profile_buckets = _build_audio_folders_and_profiles(all_qs)
    all_sons_list = list(all_qs)
    title_folders, son_to_slug = _build_audio_title_folders(all_sons_list)

    counts_map = {}
    compact_tracks = []
    for s in all_sons_list:
        audio_url = ''
        if s.lien_audio_externe:
            audio_url = s.lien_audio_externe
        elif s.fichier_audio:
            try:
                audio_url = s.fichier_audio.url
            except Exception:
                audio_url = ''
        if not audio_url:
            continue
        raw_auteur = (s.auteur_voix or '').strip()
        if _is_bassirou_khelcom_author(raw_auteur):
            cat = 'BASSIROU_KHELCOM'
            auteur = 'Serigne Bassirou Mbacké Khelcom'
        else:
            cat = (s.categorie or 'KHASSIDA').upper()
            auteur = raw_auteur or cat_labels.get(cat, 'Collection SDM')
        counts_map[cat] = counts_map.get(cat, 0) + 1
        compact_tracks.append([
            s.id,
            s.titre or 'Sans titre',
            auteur,
            cat,
            audio_url,
            son_to_slug.get(s.id, 'autres-khassidas'),
        ])

    data = {
        'folders_tree': folders_tree,
        'collections_profiles': collections_profiles,
        'profile_buckets': profile_buckets,
        'title_folders': title_folders,
        'counts_map': counts_map,
        'total_all_sons': len(compact_tracks),
        'compact_tracks': compact_tracks,
    }
    cache.set('sdm_audio_catalog_v3', data, 300)
    return data


# --- VUES PRINCIPALES ---

def home(request):
    """Page d'accueil mobile ultra-rapide avec cache mémoire des agrégats publics."""
    import datetime

    today_key = datetime.date.today().isoformat()
    pub_cache_key = f'sdm_home_public_v2_{today_key}'
    pub = cache.get(pub_cache_key)

    if pub is None:
        tous_les_contenus = ContenuDuJour.objects.order_by('id')
        contenu = None
        if tous_les_contenus.exists():
            jour_annee = datetime.date.today().timetuple().tm_yday
            count = tous_les_contenus.count()
            if count > 0:
                raw_contenu = tous_les_contenus[jour_annee % count]

                def parse_text(text):
                    parts = text.split('\n— ')
                    main_text = parts[0]
                    ref = parts[1] if len(parts) > 1 else ""
                    sub_parts = main_text.split('\n\n')
                    ar = sub_parts[0] if len(sub_parts) > 1 else ""
                    fr = sub_parts[1] if len(sub_parts) > 1 else sub_parts[0]
                    return {'arabe': ar, 'francais': fr, 'ref': ref}

                contenu = {
                    'verset': parse_text(raw_contenu.verset_du_jour),
                    'beuyit': parse_text(raw_contenu.beuyit_du_jour),
                    'rappel': parse_text(raw_contenu.rappel_dujour),
                }

        recents_khassidas = list(Khassida.objects.only('id', 'titre', 'auteur', 'image_couverture').order_by('-id')[:6])
        config = ParametresPriere.objects.first()
        total_khassidas = Khassida.objects.count()
        total_corans = Coran.objects.count()
        total_zikrs = Zikr.objects.count()

        catalog = _get_cached_audio_catalog()
        total_sons = catalog['total_all_sons']
        audio_folders = catalog['folders_tree']
        top_audio_profiles = catalog['collections_profiles'][:10]

        sdm_rappels_all = []
        rappels_json_path = os.path.join(settings.BASE_DIR, 'daily_rappels_sdm.json')
        if os.path.isfile(rappels_json_path):
            try:
                with open(rappels_json_path, 'r', encoding='utf-8') as rf:
                    sdm_rappels_all = json.load(rf)
            except Exception:
                sdm_rappels_all = []

        if not sdm_rappels_all and contenu:
            sdm_rappels_all = [{
                'id': 'sdm_default_1',
                'badge': 'Rappel Spirituel SDM',
                'arabe': contenu.get('verset', {}).get('arabe', ''),
                'texte': contenu.get('rappel', {}).get('francais', 'La constance dans le Zikr illumine le cœur.'),
                'source': contenu.get('rappel', {}).get('ref', 'SDM · Sagesse'),
                'theme_image': '/static/images/sdm_rappels/sdm_touba_emerald.jpg',
            }]

        rappel_du_jour_index = 0
        rappel_du_jour_sdm = None
        if sdm_rappels_all:
            day_num = datetime.date.today().toordinal()
            rappel_du_jour_index = day_num % len(sdm_rappels_all)
            rappel_du_jour_sdm = sdm_rappels_all[rappel_du_jour_index]

        pub = {
            'contenu': contenu,
            'recents': recents_khassidas,
            'config': config,
            'total_khassidas': total_khassidas,
            'total_corans': total_corans,
            'total_sons': total_sons,
            'total_zikrs': total_zikrs,
            'audio_folders': audio_folders,
            'top_audio_profiles': top_audio_profiles,
            'rappel_du_jour_sdm': rappel_du_jour_sdm,
            'sdm_rappels_json': json.dumps(sdm_rappels_all, ensure_ascii=False, separators=(',', ':')),
            'rappel_du_jour_index': rappel_du_jour_index % max(1, len(sdm_rappels_all)),
            'sdm_rappels_total': len(sdm_rappels_all),
        }
        cache.set(pub_cache_key, pub, 300)

    # Données réservées aux utilisateurs connectés
    derniere_lecture = None
    dernier_son = None
    wird_mahuz = None
    wird_en_cours = None
    total_zikr_user = 0
    niveau_spirituel = 1
    total_ecoutes = 0

    if request.user.is_authenticated:
        derniere_progression = ProgressionLecture.objects.filter(user=request.user).order_by('-derniere_mise_a_jour').first()
        if derniere_progression and derniere_progression.content_object:
            derniere_lecture = {
                'obj': derniere_progression.content_object,
                'page': derniere_progression.page_actuelle,
                'categorie': 'coran' if isinstance(derniere_progression.content_object, Coran) else 'khassida'
            }

        try:
            son_ct = ContentType.objects.get_for_model(Son)
            dernier_historique_son = Historique.objects.filter(user=request.user, content_type=son_ct).order_by('-date_lecture').first()
            dernier_son = dernier_historique_son.content_object if dernier_historique_son else None
        except Exception:
            dernier_son = None

        zikr_aggr = HistoriqueZikr.objects.filter(user=request.user).aggregate(total=Sum('nombre_total'))
        total_zikr_user = zikr_aggr['total'] or 0
        wird_mahuz = Wird.objects.filter(titre__icontains='Mahuz').first()
        wird_en_cours = ProgressionWird.objects.filter(user=request.user).order_by('-derniere_modif').first()
        total_ecoutes = Historique.objects.filter(user=request.user).count()
        points = (total_zikr_user // 100) + total_ecoutes
        niveau_spirituel = 1 + (points // 50)

    sdm_card_themes = [
        {'id': 'touba', 'label': 'Touba', 'src': '/static/images/sdm_rappels/sdm_touba_emerald.jpg', 'thumb': '/static/images/sdm_rappels/thumbs/sdm_touba_emerald.jpg'},
        {'id': 'parchemin', 'label': 'Parchemin', 'src': '/static/images/sdm_rappels/sdm_parchemin_royal.jpg', 'thumb': '/static/images/sdm_rappels/thumbs/sdm_parchemin_royal.jpg'},
        {'id': 'medine', 'label': 'Médine', 'src': '/static/images/sdm_rappels/sdm_nuit_medine.jpg', 'thumb': '/static/images/sdm_rappels/thumbs/sdm_nuit_medine.jpg'},
        {'id': 'kaaba', 'label': 'Or Noir', 'src': '/static/images/sdm_rappels/sdm_kaaba_or.jpg', 'thumb': '/static/images/sdm_rappels/thumbs/sdm_kaaba_or.jpg'},
        {'id': 'jade', 'label': 'Firdaws', 'src': '/static/images/sdm_rappels/sdm_firdaws_jade.jpg', 'thumb': '/static/images/sdm_rappels/thumbs/sdm_firdaws_jade.jpg'},
        {'id': 'soufi', 'label': 'Aurore', 'src': '/static/images/sdm_rappels/sdm_sufi_dawn.jpg', 'thumb': '/static/images/sdm_rappels/thumbs/sdm_sufi_dawn.jpg'},
    ]

    context = {
        **pub,
        'derniere_lecture': derniere_lecture,
        'dernier_son': dernier_son,
        'wird_mahuz': wird_mahuz,
        'wird_en_cours': wird_en_cours,
        'total_zikr_user': total_zikr_user,
        'niveau_spirituel': niveau_spirituel,
        'total_ecoutes': total_ecoutes,
        'sdm_card_themes': sdm_card_themes,
    }
    return render(request, 'bibliotheque/index.html', context)

def liste_dynamique(request, categorie):
    """Affiche les listes filtrées par catégorie (Khassida, Coran, etc.)."""
    query = request.GET.get('search')
    template_name = 'bibliotheque/liste.html'
    items = []

    if categorie == 'khassida':
        compact_kh = cache.get('sdm_khassidas_list_v1')
        if compact_kh is None:
            compact_kh = []
            for kh in Khassida.objects.only('id', 'titre', 'auteur', 'est_premium', 'image_couverture').order_by('titre', 'id'):
                cover = ''
                if kh.image_couverture:
                    try:
                        cover = kh.image_couverture.url
                    except Exception:
                        cover = ''
                compact_kh.append([
                    kh.id,
                    kh.titre or 'Khassida',
                    kh.auteur or 'Cheikh Ahmadou Bamba',
                    1 if getattr(kh, 'est_premium', False) else 0,
                    cover,
                ])
            cache.set('sdm_khassidas_list_v1', compact_kh, 300)
        if query:
            ql = query.strip().lower()
            filtered_kh = [k for k in compact_kh if ql in k[1].lower() or ql in k[2].lower()]
        else:
            filtered_kh = compact_kh
        favoris_ids = []
        if request.user.is_authenticated:
            try:
                kh_ct = ContentType.objects.get_for_model(Khassida)
                favoris_ids = list(Favori.objects.filter(user=request.user, content_type=kh_ct).values_list('object_id', flat=True))
            except Exception:
                pass
        return render(request, template_name, {
            'items': [],
            'items_count': len(filtered_kh),
            'khassidas_json': json.dumps(filtered_kh, ensure_ascii=False, separators=(',', ':')),
            'favoris_ids_json': json.dumps(favoris_ids),
            'categorie': categorie,
            'query': query,
        })
    elif categorie == 'zikr':
        return redirect('zikr_compteur_default')
    elif categorie == 'wird':
        items = Wird.objects.all()
    elif categorie == 'coran':
        all_corans = Coran.objects.exclude(fichier_pdf='').exclude(fichier_pdf__isnull=True)
        jukkis_pdfs = list(all_corans.filter(numero__isnull=False).order_by('numero', 'id'))
        mushafs_pdfs = list(all_corans.filter(numero__isnull=True).order_by('id'))

        # Métadonnées officielles des 30 Jukkis (Juz 1 à 30) : nom arabe, sourate de début, plage de sourates
        JUKKI_INFOS = {
            1:  ("الجزء ١ · الم", "Al-Fâtiha (1) → Al-Baqara (2:141)", 1),
            2:  ("الجزء ٢ · سيقول", "Al-Baqara (2:142 → 2:252)", 2),
            3:  ("الجزء ٣ · تلك الرسل", "Al-Baqara (2:253) → Âl-'Imrân (3:92)", 3),
            4:  ("الجزء ٤ · لن تنالوا", "Âl-'Imrân (3:93) → An-Nisâ' (4:23)", 3),
            5:  ("الجزء ٥ · والمحصنات", "An-Nisâ' (4:24 → 4:147)", 4),
            6:  ("الجزء ٦ · لا يحب الله", "An-Nisâ' (4:148) → Al-Mâ'ida (5:81)", 5),
            7:  ("الجزء ٧ · وإذا سمعوا", "Al-Mâ'ida (5:82) → Al-An'âm (6:110)", 6),
            8:  ("الجزء ٨ · ولو أننا", "Al-An'âm (6:111) → Al-A'râf (7:87)", 7),
            9:  ("الجزء ٩ · قال الملأ", "Al-A'râf (7:88) → Al-Anfâl (8:40)", 7),
            10: ("الجزء ١٠ · واعلموا", "Al-Anfâl (8:41) → At-Tawba (9:92)", 8),
            11: ("الجزء ١١ · يعتذرون", "At-Tawba (9:93) → Hûd (11:5)", 10),
            12: ("الجزء ١٢ · وما من دابة", "Hûd (11:6) → Yûsuf (12:52)", 11),
            13: ("الجزء ١٣ · وما أبرئ", "Yûsuf (12:53) → Ibrâhîm (14:52)", 12),
            14: ("الجزء ١٤ · ربما", "Al-Hijr (15:1) → An-Nahl (16:128)", 15),
            15: ("الجزء ١٥ · سبحان الذي", "Al-Isrâ' (17:1) → Al-Kahf (18:74)", 17),
            16: ("الجزء ١٦ · قال ألم", "Al-Kahf (18:75) → Tâ-Hâ (20:135)", 19),
            17: ("الجزء ١٧ · اقترب", "Al-Anbiyâ' (21:1) → Al-Hajj (22:78)", 21),
            18: ("الجزء ١٨ · قد أفلح", "Al-Mu'minûn (23:1) → Al-Furqân (25:20)", 23),
            19: ("الجزء ١٩ · وقال الذين", "Al-Furqân (25:21) → An-Naml (27:55)", 26),
            20: ("الجزء ٢٠ · أمن خلق", "An-Naml (27:56) → Al-'Ankabût (29:45)", 28),
            21: ("الجزء ٢١ · اتل ما أوحي", "Al-'Ankabût (29:46) → Al-Ahzâb (33:30)", 30),
            22: ("الجزء ٢٢ · ومن يقنت", "Al-Ahzâb (33:31) → Yâ-Sîn (36:27)", 34),
            23: ("الجزء ٢٣ · وما لي", "Yâ-Sîn (36:28) → Az-Zumar (39:31)", 36),
            24: ("الجزء ٢٤ · فمن أظلم", "Az-Zumar (39:32) → Fussilat (41:46)", 40),
            25: ("الجزء ٢٥ · إليه يرد", "Fussilat (41:47) → Al-Jâthiya (45:37)", 42),
            26: ("الجزء ٢٦ · حم", "Al-Ahqâf (46:1) → Adh-Dhâriyât (51:30)", 46),
            27: ("الجزء ٢٧ · قال فما خطبكم", "Adh-Dhâriyât (51:31) → Al-Hadîd (57:29)", 55),
            28: ("الجزء ٢٨ · قد سمع الله", "Al-Mujâdala (58:1) → At-Tahrîm (66:12)", 58),
            29: ("الجزء ٢٩ · تبارك الذي", "Al-Mulk (67:1) → Al-Mursalât (77:50)", 67),
            30: ("الجزء ٣٠ · عمّ يتساءلون", "Juz Amma : An-Naba' (78) → An-Nâs (114)", 78),
        }
        jukki_by_num = {j.numero: j for j in jukkis_pdfs}
        jukkis_list = []
        for num in range(1, 31):
            ar_lbl, fr_range, start_surah = JUKKI_INFOS[num]
            doc = jukki_by_num.get(num)
            jukkis_list.append({
                'numero': num,
                'ar_label': ar_lbl,
                'fr_range': fr_range,
                'start_surah': start_surah,
                'hizb_range': f"Hizb {num * 2 - 1} – {num * 2}",
                'pdf_id': doc.id if doc else None,
                'titre': doc.titre if doc else f"Jukki {num} (Juz {num})",
            })

        return render(request, 'bibliotheque/coran_interactif.html', {
            'jukkis_list': jukkis_list,
            'mushafs_pdfs': mushafs_pdfs,
            'coran_pdfs': jukkis_pdfs + mushafs_pdfs,
            'categorie': 'coran',
        })

    if query and items:
        items = items.filter(titre__icontains=query)

    return render(request, template_name, {
        'items': items,
        'categorie': categorie,
        'query': query
    })

def lire_pdf(request, categorie, id):
    """Lecteur PDF pour le Coran et les Khassidas."""
    if categorie == 'coran':
        target_model = Coran
    else:
        target_model = Khassida
        
    if categorie == 'wird':
        from .models import Wird
        wird = get_object_or_404(Wird, id=id)
        return redirect('lire_wird', slug=wird.slug)
        
    document = get_object_or_404(target_model, id=id)

    # Vérifier l'accès Premium
    premium_block = _check_premium_access(request, document)
    if premium_block:
        return premium_block
    
    # Récupérer la progression
    page_reprise = 1
    if request.user.is_authenticated:
        content_type = ContentType.objects.get_for_model(target_model)
        prog = ProgressionLecture.objects.filter(user=request.user, content_type=content_type, object_id=id).first()
        if prog:
            page_reprise = prog.page_actuelle

    # Fetch recent sounds for background audio player (limité pour ouverture PDF instantanée)
    sons = Son.objects.only('id', 'titre', 'auteur_voix', 'categorie', 'lien_audio_externe', 'fichier_audio').order_by('-date_ajout')[:60]

    # Préparer l'URL directe du PDF comme fallback rapide (sans appel API synchrone bloquant)
    direct_pdf_url = ''
    try:
        if document.fichier_pdf:
            raw_url = document.fichier_pdf.url
            if raw_url.startswith('//'):
                direct_pdf_url = 'https:' + raw_url
            else:
                direct_pdf_url = raw_url
    except (ValueError, Exception):
        direct_pdf_url = ''

    return render(request, 'bibliotheque/lecteur.html', {
        'document': document,
        'categorie': categorie,
        'page_reprise': page_reprise,
        'sons': sons,
        'direct_pdf_url': direct_pdf_url,
    })


def _get_pdf_bytes_cached(categorie, document):
    """
    Récupère les octets du fichier PDF avec mise en cache sur disque local
    pour éviter de retélécharger le ZIP Cloudinary à chaque ouverture ou miniature.
    """
    import tempfile
    import zipfile
    import io
    import cloudinary
    import cloudinary.utils
    from django.conf import settings as conf_settings

    if not document.fichier_pdf:
        return None

    cache_dir = os.path.join(tempfile.gettempdir(), 'sdm_pdf_cache')
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"{categorie}_{document.id}.pdf")

    if os.path.exists(cache_file) and os.path.getsize(cache_file) > 500:
        try:
            with open(cache_file, 'rb') as f:
                return f.read()
        except Exception:
            pass

    try:
        pdf_url = document.fichier_pdf.url
        pdf_name = str(document.fichier_pdf)
    except (ValueError, Exception):
        return None

    # 1. Fichier local dans MEDIA_ROOT
    if pdf_url.startswith('/') and not pdf_url.startswith('//'):
        file_path = os.path.join(conf_settings.MEDIA_ROOT, pdf_name)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                data = f.read()
            return data
        return None

    # 2. Fichier distant (Cloudinary)
    cloud_config = getattr(conf_settings, 'CLOUDINARY_STORAGE', {})
    cloudinary.config(
        cloud_name=cloud_config.get('CLOUD_NAME', os.environ.get('CLOUDINARY_CLOUD_NAME', 'dcajqzg2h')),
        api_key=cloud_config.get('API_KEY', os.environ.get('CLOUDINARY_API_KEY', '')),
        api_secret=cloud_config.get('API_SECRET', os.environ.get('CLOUDINARY_API_SECRET', '')),
        secure=True,
    )

    # Tentative A : URL directe rapide si accessible
    full_direct_url = ('https:' + pdf_url) if pdf_url.startswith('//') else pdf_url
    if full_direct_url.startswith('http'):
        try:
            r_direct = requests.get(full_direct_url, timeout=12)
            if r_direct.status_code == 200 and len(r_direct.content) > 500 and r_direct.content[:4] == b'%PDF':
                with open(cache_file, 'wb') as f:
                    f.write(r_direct.content)
                return r_direct.content
        except Exception:
            pass

    # Tentative B : Contournement Cloudinary Raw via ZIP signé
    try:
        zip_url = cloudinary.utils.download_zip_url(
            public_ids=[pdf_name],
            resource_type='raw'
        )
        remote = requests.get(zip_url, timeout=25)
        if remote.status_code == 200:
            z = zipfile.ZipFile(io.BytesIO(remote.content))
            filename_in_zip = z.namelist()[0]
            pdf_data = z.read(filename_in_zip)
            if len(pdf_data) > 500:
                with open(cache_file, 'wb') as f:
                    f.write(pdf_data)
                return pdf_data
    except Exception as e:
        print(f"[_get_pdf_bytes_cached] ZIP workaround failed: {e}")

    # Tentative C : API Admin Cloudinary en dernier recours
    try:
        import cloudinary.api
        resource_info = cloudinary.api.resource(pdf_name, resource_type='raw', type='upload')
        real_url = resource_info.get('secure_url', '')
        if real_url:
            remote = requests.get(real_url, timeout=20)
            if remote.status_code == 200 and len(remote.content) > 500:
                with open(cache_file, 'wb') as f:
                    f.write(remote.content)
                return remote.content
    except Exception as e:
        print(f"[_get_pdf_bytes_cached] API fallback failed: {e}")

    return None


def proxy_pdf(request, categorie, id):
    """Proxy ultra-rapide avec cache disque serveur pour les PDF."""
    target_model = Coran if categorie == 'coran' else Khassida
    document = get_object_or_404(target_model, id=id)

    if request.user.is_authenticated:
        try:
            content_type = ContentType.objects.get_for_model(target_model)
            Telechargement.objects.get_or_create(
                user=request.user,
                content_type=content_type,
                object_id=id
            )
        except Exception:
            pass

    pdf_data = _get_pdf_bytes_cached(categorie, document)
    if pdf_data:
        res = HttpResponse(pdf_data, content_type='application/pdf')
        res['Access-Control-Allow-Origin'] = '*'
        res['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        res['Cache-Control'] = 'public, max-age=604800, immutable'
        safe_title = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in document.titre)
        res['Content-Disposition'] = f'inline; filename="{safe_title}.pdf"'
        return res

    return HttpResponse(
        "Impossible de charger le PDF. Le fichier est restreint ou temporairement indisponible.",
        status=502
    )


def thumb_pdf(request, categorie, id):
    """
    Extrait et renvoie l'image JPEG réelle de la 1re page (Page 1) du PDF
    avec mise en cache disque et navigateur longue durée.
    """
    import tempfile
    import io

    target_model = Coran if categorie == 'coran' else Khassida
    document = get_object_or_404(target_model, id=id)
    is_hd = request.GET.get('hd') == '1'

    thumb_dir = os.path.join(tempfile.gettempdir(), 'sdm_thumb_cache')
    os.makedirs(thumb_dir, exist_ok=True)
    suffix = 'hd' if is_hd else 'sm'
    thumb_path = os.path.join(thumb_dir, f"{categorie}_{id}_p1_{suffix}.jpg")

    if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 300:
        try:
            with open(thumb_path, 'rb') as f:
                res = HttpResponse(f.read(), content_type='image/jpeg')
                res['Cache-Control'] = 'public, max-age=31536000, immutable'
                res['Access-Control-Allow-Origin'] = '*'
                return res
        except Exception:
            pass

    pdf_data = _get_pdf_bytes_cached(categorie, document)
    if pdf_data:
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            if doc.page_count > 0:
                page = doc.load_page(0)  # 1re page du PDF
                rect = page.rect
                target_w = 680.0 if is_hd else 300.0
                scale = max(0.5, min(2.5, target_w / max(rect.width, 1.0)))
                pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
                jpg_bytes = pix.tobytes("jpeg", jpg_quality=84 if is_hd else 76)
                doc.close()

                with open(thumb_path, 'wb') as f:
                    f.write(jpg_bytes)

                # Sauvegarde PERMANENTE dans la base de données Supabase + Cloudinary (pour l'éternité)
                if not is_hd and categorie == 'khassida' and not document.image_couverture:
                    def _persist_cover_forever(doc_id, raw_jpg):
                        try:
                            import cloudinary.uploader
                            up = cloudinary.uploader.upload(
                                raw_jpg,
                                folder="couvertures_page1",
                                public_id=f"khassida_{doc_id}_page1",
                                overwrite=True,
                                resource_type="image"
                            )
                            sec_url = up.get('secure_url')
                            if sec_url:
                                Khassida.objects.filter(id=doc_id).update(image_couverture=sec_url)
                        except Exception:
                            pass
                    import threading
                    threading.Thread(target=_persist_cover_forever, args=(document.id, jpg_bytes), daemon=True).start()

                res = HttpResponse(jpg_bytes, content_type='image/jpeg')
                res['Cache-Control'] = 'public, max-age=31536000, immutable'
                res['Access-Control-Allow-Origin'] = '*'
                return res
        except Exception as e:
            print(f"[thumb_pdf] PyMuPDF error: {e}")

    # Fallback PIL : génère une image JPEG enluminée de 1re page si le PDF distant est hors-ligne
    try:
        from PIL import Image, ImageDraw
        w, h = (480, 660) if is_hd else (260, 360)
        img = Image.new('RGB', (w, h), color=(248, 237, 211))
        draw = ImageDraw.Draw(img)
        draw.rectangle([6, 6, w - 7, h - 7], outline=(196, 148, 39), width=3)
        draw.rectangle([14, 14, w - 15, h - 15], outline=(16, 120, 80), width=1)
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=80)
        res = HttpResponse(buf.getvalue(), content_type='image/jpeg')
        res['Cache-Control'] = 'public, max-age=3600'
        return res
    except Exception:
        return HttpResponse(status=404)

@csrf_exempt
def sauvegarder_progression_pdf(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'ignored', 'message': 'Non connecté'}, status=200)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            categorie = data.get('categorie')
            doc_id = data.get('id')
            page = data.get('page')

            if not all([categorie, doc_id, page]):
                return JsonResponse({'status': 'error', 'message': 'Données manquantes'}, status=400)

            target_model = Coran if categorie == 'coran' else Khassida
            document = get_object_or_404(target_model, id=doc_id)
            content_type = ContentType.objects.get_for_model(target_model)

            progression, created = ProgressionLecture.objects.get_or_create(
                user=request.user,
                content_type=content_type,
                object_id=document.id,
                defaults={'page_actuelle': page}
            )
            
            if not created:
                progression.page_actuelle = page
                progression.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

# --- GESTION DU ZIKR ---

DEFAULT_ZIKRS_SEED = [
    {
        "titre": "Lâ ilâha illallâh",
        "texte_arabe": "لَا إِلَٰهَ إِلَّا ٱللَّٰهُ",
        "transcription": "Lâ ilâha illallâh (Il n'y a de divinité digne d'adoration qu'Allah)",
        "objectif_par_defaut": 100,
    },
    {
        "titre": "Astaghfiroullâh",
        "texte_arabe": "أَسْتَغْفِرُ ٱللَّٰهَ",
        "transcription": "Astaghfiroullâh al-'Azîm (Je demande pardon à Allah)",
        "objectif_par_defaut": 100,
    },
    {
        "titre": "Salâtou 'alâ Nabî (Salâtoul Fâtihi)",
        "texte_arabe": "ٱللَّٰهُمَّ صَلِّ عَلَىٰ سَيِّدِنَا مُحَمَّدٍ ٱلْفَاتِحِ لِمَا أُغْلِقَ",
        "transcription": "Allâhoumma salli 'alâ Sayyidinâ Mouhammadin al-Fâtihi limâ oughliqa",
        "objectif_par_defaut": 100,
    },
    {
        "titre": "SoubhânAllâh",
        "texte_arabe": "سُبْحَانَ ٱللَّٰهِ",
        "transcription": "SoubhânAllâh (Gloire et pureté à Allah)",
        "objectif_par_defaut": 33,
    },
    {
        "titre": "Alhamdoulillâh",
        "texte_arabe": "ٱلْحَمْدُ لِلَّٰهِ",
        "transcription": "Alhamdoulillâh (Louange à Allah)",
        "objectif_par_defaut": 33,
    },
    {
        "titre": "Allâhou Akbar",
        "texte_arabe": "ٱللَّٰهُ أَكْبَرُ",
        "transcription": "Allâhou Akbar (Allah est le Plus Grand)",
        "objectif_par_defaut": 33,
    },
    {
        "titre": "Hasbounallâhou wa ni'mal Wakîl",
        "texte_arabe": "حَسْبُنَا ٱللَّٰهُ وَنِعْمَ ٱلْوَكِيلُ",
        "transcription": "Hasbounallâhou wa ni'mal Wakîl (Allah nous suffit, Il est notre meilleur Garant)",
        "objectif_par_defaut": 313,
    },
]


def _ensure_default_zikrs():
    try:
        # Supprimer ou corriger les anciens Zikrs de test incomplets ('salatou', 'salaat')
        Zikr.objects.filter(titre__in=['salatou', 'salaat'], texte_arabe='').delete()
        existing_titles = set(Zikr.objects.values_list('titre', flat=True))
        for item in DEFAULT_ZIKRS_SEED:
            if item["titre"] not in existing_titles:
                Zikr.objects.create(
                    titre=item["titre"],
                    texte_arabe=item["texte_arabe"],
                    transcription=item["transcription"],
                    objectif_par_defaut=item["objectif_par_defaut"],
                )
    except Exception:
        pass


@csrf_exempt
def api_supprimer_zikr(request, zikr_id):
    """Supprime un Zikr personnalisé de la base de données."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)
    try:
        Zikr.objects.filter(id=zikr_id).delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def zikr_compteur(request, id=None):
    """Interface complète du Chapelet Électronique & Gestionnaire de Zikrs et Objectifs."""
    _ensure_default_zikrs()

    if id:
        zikr = get_object_or_404(Zikr, id=id)
    else:
        zikr = Zikr.objects.first()
        if not zikr:
            zikr = Zikr.objects.create(
                titre="Lâ ilâha illallâh",
                texte_arabe="لَا إِلَٰهَ إِلَّا ٱللَّٰهُ",
                transcription="Il n'y a de divinité qu'Allah",
                objectif_par_defaut=100,
            )

    if hasattr(zikr, 'est_premium') and getattr(zikr, 'id', 0) != 0:
        premium_block = _check_premium_access(request, zikr)
        if premium_block:
            return premium_block

    tous_les_zikrs = list(Zikr.objects.all().order_by('id'))
    historique_recent = []
    total_grains_user = 0
    if request.user.is_authenticated:
        historique_recent = list(
            HistoriqueZikr.objects.filter(user=request.user)
            .select_related('zikr')
            .order_by('-date_seance')[:10]
        )
        total_grains_user = (
            HistoriqueZikr.objects.filter(user=request.user)
            .aggregate(total=Sum('nombre_total'))['total'] or 0
        )

    return render(request, 'bibliotheque/zikr_compteur.html', {
        'zikr': zikr,
        'tous_les_zikrs': tous_les_zikrs,
        'historique_recent': historique_recent,
        'total_grains_user': total_grains_user,
    })


@csrf_exempt
def api_creer_zikr(request):
    """
    Crée ou met à jour un Zikr ET son Objectif simultanément en base de données.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

    try:
        data = json.loads(request.body or '{}')
        titre = (data.get('titre') or data.get('nom') or '').strip()
        texte_arabe = (data.get('texte_arabe') or data.get('arabe') or '').strip()
        transcription = (data.get('transcription') or data.get('trans') or '').strip()
        try:
            objectif = max(1, int(data.get('objectif') or data.get('goal') or 33))
        except (ValueError, TypeError):
            objectif = 33

        if not titre:
            return JsonResponse({'status': 'error', 'message': 'Veuillez saisir le nom du Zikr.'}, status=400)

        zikr, created = Zikr.objects.get_or_create(
            titre=titre,
            defaults={
                'texte_arabe': texte_arabe,
                'transcription': transcription,
                'objectif_par_defaut': objectif,
            }
        )
        if not created:
            zikr.objectif_par_defaut = objectif
            if texte_arabe:
                zikr.texte_arabe = texte_arabe
            if transcription:
                zikr.transcription = transcription
            zikr.save()

        return JsonResponse({
            'status': 'success',
            'created': created,
            'zikr': {
                'id': zikr.id,
                'nom': zikr.titre,
                'arabe': zikr.texte_arabe or '',
                'trans': zikr.transcription or '',
                'goal': zikr.objectif_par_defaut,
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt
def api_modifier_objectif_zikr(request):
    """
    Enregistre immédiatement un nouvel objectif pour un Zikr existant ou personnalisé.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

    try:
        data = json.loads(request.body or '{}')
        zikr_id = data.get('zikr_id')
        nom_salat = (data.get('nom_salat') or '').strip()
        objectif = max(1, int(data.get('objectif') or 33))

        zikr = None
        if zikr_id and str(zikr_id).isdigit() and int(zikr_id) > 0:
            zikr = Zikr.objects.filter(id=int(zikr_id)).first()
        if not zikr and nom_salat:
            zikr, _ = Zikr.objects.get_or_create(
                titre=nom_salat,
                defaults={'objectif_par_defaut': objectif}
            )
        if zikr:
            zikr.objectif_par_defaut = objectif
            zikr.save(update_fields=['objectif_par_defaut'])

        return JsonResponse({
            'status': 'success',
            'objectif': objectif,
            'zikr_id': zikr.id if zikr else 0,
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt
def enregistrer_seance(request):
    """API pour sauvegarder une séance de Zikr (à tout moment ou à la fin de l'objectif)."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body or '{}')
            zikr_id = data.get('zikr_id')
            nom_salat = (data.get('nom_salat') or '').strip()
            arabe = (data.get('arabe') or '').strip()
            trans = (data.get('trans') or '').strip()
            total = int(data.get('total') or 0)
            objectif = max(1, int(data.get('objectif') or 33))

            if total <= 0:
                return JsonResponse({'status': 'error', 'message': 'Faites au moins 1 répétition avant d\'enregistrer.'}, status=400)

            zikr = None
            if nom_salat:
                zikr = Zikr.objects.filter(titre__iexact=nom_salat).first()
            if not zikr and zikr_id and str(zikr_id).isdigit() and int(zikr_id) > 0:
                zikr = Zikr.objects.filter(id=int(zikr_id)).first()
            if not zikr:
                zikr = Zikr.objects.create(
                    titre=nom_salat or "Zikr Personnel",
                    texte_arabe=arabe,
                    transcription=trans,
                    objectif_par_defaut=objectif,
                )
            else:
                if zikr.objectif_par_defaut != objectif:
                    zikr.objectif_par_defaut = objectif
                    zikr.save(update_fields=['objectif_par_defaut'])

            if request.user.is_authenticated:
                seance = HistoriqueZikr.objects.create(
                    user=request.user,
                    zikr=zikr,
                    nombre_total=total
                )
                total_cumule = (
                    HistoriqueZikr.objects.filter(user=request.user)
                    .aggregate(t=Sum('nombre_total'))['t'] or total
                )
                return JsonResponse({
                    'status': 'success',
                    'saved_in_db': True,
                    'zikr_id': zikr.id,
                    'zikr_titre': zikr.titre,
                    'total': total,
                    'total_cumule': total_cumule,
                    'date': seance.date_seance.strftime('%d/%m/%Y %H:%M'),
                })
            else:
                return JsonResponse({
                    'status': 'success',
                    'saved_in_db': False,
                    'zikr_id': zikr.id,
                    'zikr_titre': zikr.titre,
                    'total': total,
                    'date': timezone.now().strftime('%d/%m/%Y %H:%M'),
                    'message': 'Séance enregistrée sur votre appareil !'
                })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

# --- GESTION DES SONS ---

def liste_sons(request):
    """Audiothèque mobile ultra-rapide : catalogue en cache mémoire + rendu virtuel JS instantané (0 rechargement par dossier/profil)."""
    categorie_filter = (request.GET.get('cat') or '').strip().upper() or None
    profil_filter = (request.GET.get('profil') or '').strip() or None
    oeuvre_filter = (request.GET.get('oeuvre') or '').strip().lower() or None

    catalog = _get_cached_audio_catalog()
    all_folders = catalog['folders_tree']
    all_tracks = catalog['compact_tracks']
    title_folders = catalog['title_folders']
    counts_map = catalog['counts_map']
    total_all_sons = catalog['total_all_sons']

    if categorie_filter:
        matched_folder = next((f for f in all_folders if f['code'] == categorie_filter), None)
        collections_profiles = matched_folder['profiles'] if matched_folder else []
        profile_buckets = {p['nom'].lower(): p for p in collections_profiles}
        base_tracks = [t for t in all_tracks if t[3] == categorie_filter]
    else:
        collections_profiles = catalog['collections_profiles']
        profile_buckets = catalog['profile_buckets']
        base_tracks = all_tracks

    active_profil_obj = profile_buckets.get(profil_filter.lower()) if profil_filter else None
    active_folder_meta = AUDIO_FOLDER_META.get(categorie_filter) if categorie_filter else None
    active_oeuvre_obj = next((tf for tf in title_folders if tf['slug'] == oeuvre_filter), None) if oeuvre_filter else None

    if profil_filter:
        pf_low = profil_filter.lower()
        filtered_tracks = sorted([t for t in base_tracks if t[2].lower() == pf_low], key=lambda x: x[1].lower())
    elif oeuvre_filter:
        filtered_tracks = [t for t in base_tracks if t[5] == oeuvre_filter]
    else:
        filtered_tracks = base_tracks

    categories = Son.CATEGORIES
    all_cat_pairs = [('KHASSIDA', 'Khassidas & Kourels'), ('BASSIROU_KHELCOM', 'Serigne Bassirou Mbacké Khelcom')] + [
        (code, label) for code, label in Son.CATEGORIES if code != 'KHASSIDA'
    ]
    categories_with_counts = [
        (code, AUDIO_FOLDER_META.get(code, {}).get('label', label), counts_map.get(code, 0))
        for code, label in all_cat_pairs
    ]

    favoris_ids = []
    if request.user.is_authenticated:
        try:
            son_ct = ContentType.objects.get_for_model(Son)
            favoris_ids = list(Favori.objects.filter(user=request.user, content_type=son_ct).values_list('object_id', flat=True))
        except Exception:
            pass

    return render(request, 'bibliotheque/liste_sons.html', {
        'sons_count': len(filtered_tracks),
        'sons_json': json.dumps(filtered_tracks, ensure_ascii=False, separators=(',', ':')),
        'all_tracks_json': json.dumps(all_tracks, ensure_ascii=False, separators=(',', ':')),
        'folders_tree_json': json.dumps(all_folders, ensure_ascii=False, separators=(',', ':')),
        'title_folders_json': json.dumps(title_folders, ensure_ascii=False, separators=(',', ':')),
        'favoris_ids_json': json.dumps(favoris_ids),
        'categories': categories,
        'categories_with_counts': categories_with_counts,
        'folders_tree': all_folders,
        'title_folders': title_folders,
        'active_folder_meta': active_folder_meta,
        'collections_profiles': collections_profiles,
        'active_profil': profil_filter,
        'active_profil_obj': active_profil_obj,
        'active_oeuvre': oeuvre_filter,
        'active_oeuvre_obj': active_oeuvre_obj,
        'total_all_sons': total_all_sons,
        'active_cat': categorie_filter,
        'favoris_ids': favoris_ids,
    })

def run_import_xamxam(request):
    """View to trigger the xamxam audio import directly from the web."""
    from django.core.management import call_command
    import threading
    
    def run_cmd():
        call_command('import_xamxam')
        
    thread = threading.Thread(target=run_cmd)
    thread.start()
    return HttpResponse("Import XamXam démarré en arrière-plan. Vérifiez les sons dans quelques minutes.")


def _extract_telegram_audio_info(tg_url):
    """
    Extrait le flux audio (MP3/OGG/M4A) et le titre depuis un lien Telegram public (https://t.me/<canal>/<id>).
    Retourne (audio_url, extracted_title, extracted_author) ou (None, None, None).
    """
    import re
    import html as html_lib
    try:
        m = re.search(r't\.me/(?:s/)?([A-Za-z0-9_]+)/(\d+)', tg_url)
        if not m:
            return None, None, None
        channel, post_id = m.group(1), m.group(2)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
        }
        for candidate_url in [
            f"https://t.me/{channel}/{post_id}?embed=1&mode=tme",
            f"https://t.me/s/{channel}/{post_id}",
        ]:
            resp = requests.get(candidate_url, headers=headers, timeout=15)
            if resp.status_code != 200:
                continue
            page = resp.text

            # Chercher une source audio ou voice/video directe dans l'embed Telegram
            media_match = (
                re.search(r'<audio[^>]+src=["\']([^"\']+)["\']', page)
                or re.search(r'data-audio=["\']([^"\']+)["\']', page)
                or re.search(r'<source[^>]+src=["\'](https://[^"\']+\.(?:mp3|m4a|ogg|opus|wav|aac)[^"\']*)["\']', page, re.I)
                or re.search(r'(https://cdn\d*\.telesco\.pe/file/[^"\'\s<>]+)', page)
                or re.search(r'(https://[^"\'\s<>]+telesco\.pe/file/[^"\'\s<>]+)', page)
                or re.search(r'<video[^>]+src=["\'](https://[^"\']+)["\']', page)
            )
            if media_match:
                media_url = html_lib.unescape(media_match.group(1))
                title_match = re.search(r'class=["\']tgme_widget_message_audio_title["\'][^>]*>([^<]+)<', page)
                perf_match = re.search(r'class=["\']tgme_widget_message_audio_performer["\'][^>]*>([^<]+)<', page)
                text_match = re.search(r'class=["\']tgme_widget_message_text[^"\']*["\'][^>]*>(.*?)</div>', page, re.S)
                ext_title = html_lib.unescape(title_match.group(1)).strip() if title_match else ''
                ext_author = html_lib.unescape(perf_match.group(1)).strip() if perf_match else f"Telegram @{channel}"
                if not ext_title and text_match:
                    clean_txt = re.sub(r'<[^>]+>', ' ', text_match.group(1))
                    ext_title = html_lib.unescape(clean_txt).strip()[:90]
                return media_url, (ext_title or f"Audio Telegram {channel} #{post_id}"), ext_author
    except Exception:
        pass
    return None, None, None


def _is_catalog_admin(user):
    return bool(user and user.is_authenticated and (user.is_staff or user.is_superuser))


def api_ajouter_son(request):
    """
    RESERVE STRICTEMENT A L'ADMINISTRATEUR (is_staff / is_superuser).
    Ajoute un ou plusieurs sons (depuis fichiers audio ou lien direct) sur Cloudinary (resource_type='video').
    """
    if not _is_catalog_admin(request.user):
        return JsonResponse({'status': 'error', 'message': "Accès interdit : réservé à l'administrateur."}, status=403)
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

    try:
        import cloudinary.uploader
        import re

        titre_saisi = (request.POST.get('titre') or '').strip()
        auteur_saisi = (request.POST.get('auteur_voix') or '').strip() or 'Kourel / Telegram'
        categorie = (request.POST.get('categorie') or 'KHASSIDA').strip().upper()
        valid_cats = {c[0] for c in Son.CATEGORIES}
        if categorie not in valid_cats:
            categorie = 'KHASSIDA'

        lien = (request.POST.get('lien_audio') or '').strip()
        fichiers = request.FILES.getlist('fichiers_audio') or request.FILES.getlist('fichier_audio')

        created_sons = []

        # Cas 1 : Fichiers audio envoyés depuis le téléphone / PC (ex: audios téléchargés depuis Telegram)
        if fichiers:
            for idx, f in enumerate(fichiers):
                raw_name = os.path.splitext(f.name)[0]
                ext = os.path.splitext(f.name)[1].lower() or '.mp3'
                clean_name = re.sub(r'[_\-]+', ' ', raw_name).strip()
                track_title = titre_saisi if (titre_saisi and len(fichiers) == 1) else (
                    f"{titre_saisi} ({idx + 1})" if titre_saisi else (clean_name or "Son Telegram")
                )

                secure_url = ''
                # 1. Essayer Cloudinary (resource_type='video' pour streaming Range HTTP)
                try:
                    upload_res = cloudinary.uploader.upload(
                        f,
                        resource_type='video',
                        folder=f'media/audios/{categorie.lower()}',
                        use_filename=True,
                        unique_filename=True,
                    )
                    secure_url = upload_res.get('secure_url') or ''
                except Exception:
                    secure_url = ''

                # 2. Fallback automatique en stockage local dans l'application si Cloudinary est plein/indisponible
                if not secure_url:
                    local_dir = os.path.join(settings.BASE_DIR, 'static', 'audios_locaux', categorie.lower())
                    os.makedirs(local_dir, exist_ok=True)
                    safe_slug = re.sub(r'[^a-zA-Z0-9_\-]+', '_', clean_name)[:70] or f'audio_{idx}'
                    local_fname = f"{safe_slug}_{int(timezone.now().timestamp())}{ext}"
                    local_path = os.path.join(local_dir, local_fname)
                    f.seek(0)
                    with open(local_path, 'wb+') as dest:
                        for chunk in f.chunks():
                            dest.write(chunk)
                    secure_url = f"/static/audios_locaux/{categorie.lower()}/{local_fname}"

                son = Son.objects.create(
                    titre=track_title[:200],
                    auteur_voix=auteur_saisi[:150],
                    categorie=categorie,
                    lien_audio_externe=secure_url,
                )
                created_sons.append({
                    'id': son.id,
                    'titre': son.titre,
                    'auteur': son.auteur_voix or son.get_categorie_display(),
                    'categorie': son.categorie,
                    'url': son.lien_audio_externe,
                })

        # Cas 2 : Lien Telegram (https://t.me/...) ou lien audio direct (.mp3, .m4a, .ogg...)
        elif lien:
            target_media_url = lien
            auto_title = ''
            auto_author = ''

            if 't.me/' in lien or 'telegram.me/' in lien:
                extracted_url, ext_title, ext_author = _extract_telegram_audio_info(lien)
                if not extracted_url:
                    return JsonResponse({
                        'status': 'error',
                        'message': (
                            "Ce post Telegram ne contient pas de flux audio web public direct (fichier > 20 Mo ou canal privé). "
                            "Téléchargez l'audio dans Telegram puis sélectionnez-le via « Choisir un fichier Audio Telegram » ci-dessus."
                        )
                    }, status=400)
                target_media_url = extracted_url
                auto_title = ext_title or ''
                auto_author = ext_author or ''

            # Envoyer le flux distant sur Cloudinary (video/upload) pour une persistance éternelle
            try:
                upload_res = cloudinary.uploader.upload(
                    target_media_url,
                    resource_type='video',
                    folder='media/audios/telegram',
                )
                final_url = upload_res.get('secure_url') or target_media_url
            except Exception:
                final_url = target_media_url

            final_title = titre_saisi or auto_title or "Audio Telegram"
            final_author = (request.POST.get('auteur_voix') or '').strip() or auto_author or "Kourel / Telegram"

            son = Son.objects.create(
                titre=final_title[:200],
                auteur_voix=final_author[:150],
                categorie=categorie,
                lien_audio_externe=final_url,
            )
            created_sons.append({
                'id': son.id,
                'titre': son.titre,
                'auteur': son.auteur_voix or son.get_categorie_display(),
                'categorie': son.categorie,
                'url': son.lien_audio_externe,
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Veuillez sélectionner un fichier audio Telegram ou coller un lien audio.'
            }, status=400)

        _invalidate_catalog_cache()
        return JsonResponse({
            'status': 'success',
            'count': len(created_sons),
            'sons': created_sons,
            'message': f"{len(created_sons)} son(s) ajouté(s) avec succès !"
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f"Erreur lors de l'ajout : {str(e)}"}, status=400)


def api_supprimer_son(request, son_id):
    """RESERVE STRICTEMENT A L'ADMINISTRATEUR : Supprime définitivement un son de l'audiothèque."""
    if not _is_catalog_admin(request.user):
        return JsonResponse({'status': 'error', 'message': "Accès interdit : réservé à l'administrateur."}, status=403)
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)
    try:
        deleted, _ = Son.objects.filter(id=son_id).delete()
        _invalidate_catalog_cache()
        return JsonResponse({'status': 'success', 'deleted': deleted > 0, 'id': son_id})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def api_modifier_son(request, son_id):
    """RESERVE STRICTEMENT A L'ADMINISTRATEUR : Permet de renommer un son ou modifier son auteur/catégorie."""
    if not _is_catalog_admin(request.user):
        return JsonResponse({'status': 'error', 'message': "Accès interdit : réservé à l'administrateur."}, status=403)
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)
    try:
        data = json.loads(request.body or '{}')
        son = Son.objects.filter(id=son_id).first()
        if not son:
            return JsonResponse({'status': 'error', 'message': 'Son introuvable'}, status=404)

        nouveau_titre = (data.get('titre') or '').strip()
        nouvel_auteur = (data.get('auteur_voix') or '').strip()
        nouvelle_cat = (data.get('categorie') or '').strip().upper()

        if nouveau_titre:
            son.titre = nouveau_titre[:200]
        if nouvel_auteur:
            son.auteur_voix = nouvel_auteur[:150]
        valid_cats = {c[0] for c in Son.CATEGORIES}
        if nouvelle_cat in valid_cats:
            son.categorie = nouvelle_cat
        son.save()
        _invalidate_catalog_cache()

        return JsonResponse({
            'status': 'success',
            'son': {
                'id': son.id,
                'titre': son.titre,
                'auteur': son.auteur_voix or son.get_categorie_display(),
                'categorie': son.categorie,
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def api_liste_sons_json(request):
    """Retourne la playlist JSON complète pour le lecteur global persistant."""
    sons = Son.objects.all().order_by('-date_ajout')
    playlist = []
    for s in sons:
        url = s.lien_audio_externe or (s.fichier_audio.url if s.fichier_audio else '')
        if not url:
            continue
        playlist.append({
            'id': s.id,
            'titre': s.titre,
            'auteur': s.auteur_voix or s.get_categorie_display(),
            'categorie': s.categorie,
            'url': url,
        })
    return JsonResponse({'status': 'success', 'playlist': playlist})


def proxy_audio(request, son_id):
    """
    Proxy Audio CORS-safe pour le téléchargement hors-ligne fiable dans IndexedDB
    (contourne les restrictions CORS des hébergeurs audio externes comme Podcloud / MP3Quran).
    """
    from django.http import StreamingHttpResponse, FileResponse
    son = get_object_or_404(Son, id=son_id)
    url = (son.lien_audio_externe or '').strip()
    if not url and son.fichier_audio:
        url = son.fichier_audio.url

    if not url:
        return HttpResponse("Aucun fichier audio associé.", status=404)

    # Cas d'un fichier stocké localement dans /static/audios_locaux/
    if url.startswith('/static/'):
        rel_path = url[len('/static/'):].lstrip('/')
        abs_path = os.path.join(settings.BASE_DIR, 'static', rel_path)
        if os.path.isfile(abs_path):
            resp = FileResponse(open(abs_path, 'rb'), content_type='audio/mpeg')
            resp['Access-Control-Allow-Origin'] = '*'
            resp['Accept-Ranges'] = 'bytes'
            return resp
        return HttpResponse("Fichier audio local introuvable.", status=404)

    try:
        upstream = requests.get(
            url,
            stream=True,
            timeout=30,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; SDMMouride/2.0)'},
        )
        upstream.raise_for_status()
        content_type = upstream.headers.get('Content-Type') or 'audio/mpeg'
        resp = StreamingHttpResponse(
            upstream.iter_content(chunk_size=32768),
            content_type=content_type,
        )
        if upstream.headers.get('Content-Length'):
            resp['Content-Length'] = upstream.headers['Content-Length']
        resp['Access-Control-Allow-Origin'] = '*'
        resp['Cache-Control'] = 'public, max-age=604800'
        return resp
    except Exception as e:
        return HttpResponse(f"Erreur proxy audio : {e}", status=502)

# --- AUTHENTIFICATION & PROFIL ---

def login_view(request):
    """Vue de connexion sécurisée avec session persistante 365 jours (Mobile/Web)."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session.set_expiry(60 * 60 * 24 * 365)  # 365 jours
            next_url = request.GET.get('next', 'home')
            if next_url == 'home' or not next_url:
                return redirect('home')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'bibliotheque/login.html', {'form': form})

def register_view(request):
    """Gestion de l'inscription utilisateur avec session persistante 365 jours."""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = ModernRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            request.session.set_expiry(60 * 60 * 24 * 365)  # 365 jours
            return redirect('home') 
    else:
        form = ModernRegisterForm()
    return render(request, 'bibliotheque/register.html', {'form': form})


def password_reset_simple(request):
    """
    Réinitialisation simplifiée du mot de passe :
      Étape 1 : l'utilisateur saisit son email (ou nom d'utilisateur).
                Si un serveur SMTP est configuré, un code à 6 chiffres lui est envoyé ;
                sinon, passage fluide direct à la création du nouveau mot de passe.
      Étape 2 : vérification du code (si SMTP actif) + définition du nouveau mot de passe + connexion auto.
    """
    from django.contrib.auth import get_user_model
    from django.core.mail import send_mail
    import random

    User = get_user_model()
    step = request.session.get('pwd_reset_step', 'email')
    reset_uid = request.session.get('pwd_reset_uid')
    reset_email_mask = request.session.get('pwd_reset_email_mask', '')
    need_code = request.session.get('pwd_reset_need_code', False)
    error_msg = None
    info_msg = None

    if request.GET.get('restart') == '1':
        for k in ('pwd_reset_step', 'pwd_reset_uid', 'pwd_reset_code', 'pwd_reset_email_mask', 'pwd_reset_need_code'):
            request.session.pop(k, None)
        return redirect('password_reset_simple')

    if request.method == 'POST':
        action = request.POST.get('action', 'find_account')

        if action == 'find_account':
            ident = (request.POST.get('identifier') or '').strip()
            user = None
            if ident:
                user = User.objects.filter(email__iexact=ident).first() or User.objects.filter(username__iexact=ident).first()
            if not user:
                error_msg = "Aucun compte trouvé avec cet email ou ce nom d'utilisateur."
            else:
                code = f"{random.randint(100000, 999999)}"
                email_sent = False
                smtp_configured = bool(getattr(settings, 'EMAIL_HOST_USER', '') and getattr(settings, 'EMAIL_HOST_PASSWORD', ''))
                if smtp_configured and user.email:
                    try:
                        send_mail(
                            subject="SDM Mouride — Code de réinitialisation de mot de passe",
                            message=f"Assalamou Alaykoum {user.username},\n\nVoici votre code de vérification SDM : {code}\n\nSi vous n'êtes pas à l'origine de cette demande, ignorez cet email.",
                            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', settings.EMAIL_HOST_USER),
                            recipient_list=[user.email],
                            fail_silently=False,
                        )
                        email_sent = True
                    except Exception:
                        email_sent = False

                em = user.email or user.username
                mask = (em[:2] + '***' + em[em.find('@'):]) if '@' in em else (em[:2] + '***')
                request.session['pwd_reset_uid'] = user.id
                request.session['pwd_reset_code'] = code
                request.session['pwd_reset_email_mask'] = mask
                request.session['pwd_reset_need_code'] = email_sent
                request.session['pwd_reset_step'] = 'new_password'
                step = 'new_password'
                reset_uid = user.id
                reset_email_mask = mask
                need_code = email_sent
                info_msg = (
                    f"Un code à 6 chiffres a été envoyé à {mask}. Saisissez-le avec votre nouveau mot de passe."
                    if email_sent else
                    f"Compte trouvé ({mask}) ! Choisissez directement votre nouveau mot de passe ci-dessous."
                )

        elif action == 'set_password' and reset_uid:
            user = User.objects.filter(id=reset_uid).first()
            p1 = (request.POST.get('new_password1') or '').strip()
            p2 = (request.POST.get('new_password2') or '').strip()
            code_in = (request.POST.get('code') or '').strip()
            expected_code = request.session.get('pwd_reset_code', '')

            if not user:
                error_msg = "Session expirée. Veuillez recommencer."
                step = 'email'
            elif need_code and code_in != expected_code:
                error_msg = "Le code de vérification saisi est incorrect."
            elif len(p1) < 6:
                error_msg = "Le nouveau mot de passe doit contenir au moins 6 caractères."
            elif p1 != p2:
                error_msg = "Les deux mots de passe ne correspondent pas."
            else:
                user.set_password(p1)
                user.save()
                for k in ('pwd_reset_step', 'pwd_reset_uid', 'pwd_reset_code', 'pwd_reset_email_mask', 'pwd_reset_need_code'):
                    request.session.pop(k, None)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                request.session.set_expiry(60 * 60 * 24 * 365)
                messages.success(request, "Votre mot de passe a été modifié avec succès. Bienvenue !")
                return redirect('home')

    return render(request, 'bibliotheque/password_reset_simple.html', {
        'step': step,
        'email_mask': reset_email_mask,
        'need_code': need_code,
        'error_msg': error_msg,
        'info_msg': info_msg,
    })

@csrf_exempt
def api_restore_session(request):
    """
    Restaure automatiquement la session Django à partir du jeton signé
    stocké dans localStorage sur mobile (Android / iOS / WebView / PWA).
    """
    from .debug_middleware import verify_persistent_auth_token, create_persistent_auth_token, PERSISTENT_AUTH_MAX_AGE
    from django.contrib.auth import get_user_model

    if request.user.is_authenticated:
        token = create_persistent_auth_token(request.user.id)
        return JsonResponse({
            'status': 'authenticated',
            'username': request.user.username,
            'token': token,
        })

    token = request.GET.get('token') or request.headers.get('X-SDM-Auth-Token')
    if not token and request.method == 'POST':
        try:
            body = json.loads(request.body or '{}')
            token = body.get('token')
        except Exception:
            token = request.POST.get('token')

    uid = verify_persistent_auth_token(token)
    if uid:
        User = get_user_model()
        user = User.objects.filter(id=uid, is_active=True).first()
        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            request.session.set_expiry(PERSISTENT_AUTH_MAX_AGE)
            new_token = create_persistent_auth_token(user.id)
            res = JsonResponse({
                'status': 'restored',
                'username': user.username,
                'token': new_token,
            })
            res.set_cookie(
                'sdm_remember_token',
                new_token,
                max_age=PERSISTENT_AUTH_MAX_AGE,
                httponly=False,
                samesite='Lax',
            )
            return res

    return JsonResponse({'status': 'anonymous'}, status=200)

@login_required
def profil_view(request):
    """Page de profil utilisateur avec modification des infos, mot de passe et statistiques spirituelles."""
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_saved_msg = None
    profile_error_msg = None

    if request.method == 'POST' and request.POST.get('action') == 'update_profile':
        new_username = (request.POST.get('username') or '').strip()
        new_first = (request.POST.get('first_name') or '').strip()
        new_last = (request.POST.get('last_name') or '').strip()
        new_email = (request.POST.get('email') or '').strip()
        new_ville = (request.POST.get('ville') or '').strip()
        new_pwd = (request.POST.get('new_password') or '').strip()

        u = request.user
        if new_username and new_username != u.username:
            if User.objects.filter(username__iexact=new_username).exclude(id=u.id).exists():
                profile_error_msg = "Ce nom d'utilisateur est déjà pris par un autre compte."
            else:
                u.username = new_username
        if not profile_error_msg:
            u.first_name = new_first[:80]
            u.last_name = new_last[:80]
            if new_email:
                u.email = new_email[:150]
            if new_pwd:
                if len(new_pwd) < 6:
                    profile_error_msg = "Le nouveau mot de passe doit contenir au moins 6 caractères."
                else:
                    u.set_password(new_pwd)
            if not profile_error_msg:
                u.save()
                if new_pwd:
                    login(request, u, backend='django.contrib.auth.backends.ModelBackend')
                if hasattr(profile, 'ville') and new_ville:
                    profile.ville = new_ville[:100]
                    profile.save(update_fields=['ville'])
                profile_saved_msg = "Vos informations de profil ont été mises à jour ✓"

    # Stats Zikr
    zikr_stats = HistoriqueZikr.objects.filter(user=request.user).aggregate(
        total=Sum('nombre_total'),
        nb_seances=Count('id')
    )
    total_zikr = zikr_stats['total'] or 0
    nb_seances_zikr = zikr_stats['nb_seances'] or 0

    # Wird complétés
    wird_completes = HistoriqueWird.objects.filter(user=request.user, complete=True).count()
    wird_en_cours = ProgressionWird.objects.filter(user=request.user).order_by('-derniere_modif').first()

    # Écoutes
    total_ecoutes = Historique.objects.filter(user=request.user).count()

    # Favoris
    nb_favoris = Favori.objects.filter(user=request.user).count()
    favoris_recents = Favori.objects.filter(user=request.user).order_by('-date_ajout')[:4]

    # Lectures terminées
    lectures_terminees = ProgressionGenerale.objects.filter(user=request.user, termine=True).count()

    # Historique récent (5 derniers)
    historique_recent = Historique.objects.filter(user=request.user).order_by('-date_lecture')[:5]

    # Streak (jours consécutifs d'activité)
    today = timezone.now().date()
    streak_jours = 0
    check_date = today
    while True:
        has_activity = (
            HistoriqueZikr.objects.filter(user=request.user, date_seance__date=check_date).exists() or
            Historique.objects.filter(user=request.user, date_lecture__date=check_date).exists()
        )
        if has_activity:
            streak_jours += 1
            check_date -= datetime.timedelta(days=1)
        else:
            break
        if streak_jours > 365:  # Safety limit
            break

    # Niveau spirituel
    points = (total_zikr // 100) + total_ecoutes + lectures_terminees
    niveau_spirituel = 1 + (points // 50)
    points_vers_prochain = points % 50
    # Progression Tazawwud
    from .models import TazawwudProgression, TazawwudLecon, TazawwudAchat, TazawwudReponseHistorique
    from .tazawwud_views import get_rappels_tazawwud
    taz_prog, _ = TazawwudProgression.objects.get_or_create(user=request.user)
    taz_prog.verifier_semaine_reset()
    total_lecons_taz = TazawwudLecon.objects.count()
    lecons_terminees_taz = taz_prog.lecons_terminees.count()
    taz_pourcentage = int((lecons_terminees_taz / total_lecons_taz * 100) if total_lecons_taz > 0 else 0)
    taz_a_forfait_complet = TazawwudAchat.a_acces_revision(request.user)
    taz_modules_payes_count = TazawwudAchat.objects.filter(user=request.user, type_achat='MODULE', statut='APPROVED').count()
    taz_nb_erreurs = TazawwudReponseHistorique.objects.filter(user=request.user, est_correct=False).count()

    context = {
        'profile': profile,
        'total_zikr': total_zikr,
        'nb_seances_zikr': nb_seances_zikr,
        'wird_completes': wird_completes,
        'wird_en_cours': wird_en_cours,
        'total_ecoutes': total_ecoutes,
        'nb_favoris': nb_favoris,
        'favoris_recents': favoris_recents,
        'lectures_terminees': lectures_terminees,
        'historique_recent': historique_recent,
        'streak_jours': streak_jours,
        'niveau_spirituel': niveau_spirituel,
        'points_vers_prochain': points_vers_prochain,
        # Tazawwud
        'taz_prog': taz_prog,
        'taz_pourcentage': taz_pourcentage,
        'taz_lecons_terminees': lecons_terminees_taz,
        'total_lecons_taz': total_lecons_taz,
        'taz_a_forfait_complet': taz_a_forfait_complet,
        'taz_modules_payes_count': taz_modules_payes_count,
        'taz_nb_erreurs': taz_nb_erreurs,
        'taz_rappel_du_jour': (get_rappels_tazawwud()[timezone.now().day % len(get_rappels_tazawwud())] if get_rappels_tazawwud() else None),
        'taz_rappels_json': json.dumps(get_rappels_tazawwud()),
        'profile_saved_msg': profile_saved_msg,
        'profile_error_msg': profile_error_msg,
    }
    return render(request, 'bibliotheque/profile.html', context)

# --- ABONNEMENT ---

@login_required
def page_abonnement(request):
    return render(request, 'bibliotheque/abonnement.html')

@login_required
def paiement_reussi(request):
    """Active le mode Premium après confirmation du paiement."""
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.est_premium = True
    profile.save()
    return redirect('home')

# --- HISTORIQUE & DÉTAILS ---

def details_contenu(request, id):
    """Affiche les détails et enregistre la consultation dans l'historique."""
    contenu = get_object_or_404(Khassida, id=id)
    if request.user.is_authenticated:
        obj_type = ContentType.objects.get_for_model(contenu)
        Historique.objects.update_or_create(
            user=request.user,
            content_type=obj_type,
            object_id=contenu.id
        )
    return render(request, 'bibliotheque/details.html', {'contenu': contenu})

@csrf_exempt
def enregistrer_ecoute_son(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'ignored', 'message': 'Non connecté'}, status=200)
    if request.method == 'POST':
        try:
            son = get_object_or_404(Son, id=id)
            obj_type = ContentType.objects.get_for_model(Son)
            Historique.objects.update_or_create(
                user=request.user,
                content_type=obj_type,
                object_id=son.id
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

def voir_historique(request):
    """Historique complet et organisé du Zikr avec total des grains et répartition."""
    historique = []
    total_grains = 0
    total_seances = 0
    par_zikr = []
    if request.user.is_authenticated:
        historique = HistoriqueZikr.objects.filter(user=request.user).select_related('zikr').order_by('-date_seance')
        total_grains = historique.aggregate(Sum('nombre_total'))['nombre_total__sum'] or 0
        total_seances = historique.count()
        par_zikr = list(
            HistoriqueZikr.objects.filter(user=request.user)
            .values('zikr__titre')
            .annotate(total=Sum('nombre_total'), seances=Count('id'))
            .order_by('-total')
        )
    return render(request, 'bibliotheque/historique.html', {
        'historique': historique,
        'total_grains': total_grains,
        'total_seances': total_seances,
        'par_zikr': par_zikr,
    })

def voir_historique_zikr(request):
    return voir_historique(request)

@login_required
def voir_historique_general(request):
    consultations = HistoriqueConsultation.objects.filter(user=request.user).order_by('-date_vue')
    return render(request, 'bibliotheque/historique_general.html', {'consultations': consultations})

def toggle_favori(request, model_name, object_id):
    from django.apps import apps
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if not request.user.is_authenticated:
        if is_ajax:
            return JsonResponse({'status': 'login_required', 'login_url': '/login/'}, status=401)
        return redirect(f"/login/?next={request.META.get('HTTP_REFERER', '/')}")
    try:
        model_class = apps.get_model('bibliotheque', model_name)
    except LookupError:
        return JsonResponse({'status': 'error'}, status=400)

    content_type = ContentType.objects.get_for_model(model_class)
    obj = get_object_or_404(model_class, id=object_id)

    favori, created = Favori.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=object_id
    )

    if not created:
        favori.delete()
        status = 'removed'
    else:
        status = 'added'

    if is_ajax:
        return JsonResponse({'status': status})

    return redirect(request.META.get('HTTP_REFERER', 'home'))

def lire_wird(request, slug):
    wird = get_object_or_404(Wird, slug=slug)

    # Vérifier l'accès Premium
    premium_block = _check_premium_access(request, wird)
    if premium_block:
        return premium_block

    etapes = wird.etapes.all().order_by('numero')
    
    progression = None
    if request.user.is_authenticated:
        progression, created = ProgressionWird.objects.get_or_create(
            user=request.user, 
            wird=wird
        )
    
    return render(request, 'bibliotheque/lire_wird.html', {
        'wird': wird,
        'etapes': etapes,
        'progression': progression,
    })

def save_wird_progress(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'ignored', 'message': 'Non connecté'}, status=200)
    if request.method == 'POST':
        data = json.loads(request.body)
        wird_id = data.get('wird_id')
        etape = data.get('etape')
        reps = data.get('reps')
        
        prog, _ = ProgressionWird.objects.get_or_create(
            user=request.user, 
            wird_id=wird_id
        )
        prog.etape_courante = etape
        prog.repetitions_faites = reps
        prog.save()
        
        return JsonResponse({'status': 'success'})

@login_required
def view_favoris(request):
    favoris = Favori.objects.filter(user=request.user)
    
    # Organize favorites by type
    favoris_by_type = {
        'Khassida': [],
        'Zikr': [],
        'Wird': [],
        'Coran': [],
        'Son': []
    }
    
    for favori in favoris:
        if favori.content_object is None:
            continue
        if favori.content_type.model == 'khassida':
            favoris_by_type['Khassida'].append(favori.content_object)
        elif favori.content_type.model == 'zikr':
            favoris_by_type['Zikr'].append(favori.content_object)
        elif favori.content_type.model == 'wird':
            favoris_by_type['Wird'].append(favori.content_object)
        elif favori.content_type.model == 'coran':
            favoris_by_type['Coran'].append(favori.content_object)
        elif favori.content_type.model == 'son':
            favoris_by_type['Son'].append(favori.content_object)
            
    context = {
        'favoris_by_type': favoris_by_type
    }
    
    return render(request, 'bibliotheque/favoris.html', context)


def view_telechargements(request):
    """
    Affiche les téléchargements hors-ligne disponibles dans l'application
    (Coffre-fort IndexedDB local + Synchronisation compte utilisateur).
    """
    telechargements_by_type = {
        'Khassida': [],
        'Coran': [],
        'Son': []
    }

    if request.user.is_authenticated:
        telechargements = Telechargement.objects.filter(user=request.user)
        for tc in telechargements:
            if tc.content_object is None:
                continue
            model_name = tc.content_type.model
            if model_name == 'khassida':
                telechargements_by_type['Khassida'].append(tc.content_object)
            elif model_name == 'coran':
                telechargements_by_type['Coran'].append(tc.content_object)
            elif model_name == 'son':
                telechargements_by_type['Son'].append(tc.content_object)

    audio_folders, _, _ = _build_audio_folders_and_profiles(Son.objects.all())
    context = {
        'telechargements_by_type': telechargements_by_type,
        'audio_folders': audio_folders,
    }

    return render(request, 'bibliotheque/telechargements.html', context)


def ajouter_telechargement(request, model_name, object_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'local_only'})
    from django.apps import apps
    try:
        model_class = apps.get_model('bibliotheque', model_name)
    except LookupError:
        return JsonResponse({'status': 'error', 'message': 'Modèle introuvable'})
        
    content_type = ContentType.objects.get_for_model(model_class)
    obj = get_object_or_404(model_class, id=object_id)
    
    telechargement, created = Telechargement.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=object_id
    )
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.META.get('HTTP_ACCEPT') == 'application/json':
        return JsonResponse({'status': 'success', 'created': created})
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))



# --- RECHERCHE GLOBALE ---

def recherche_globale(request):
    """Recherche simultanée dans tous les types de contenu."""
    query = request.GET.get('q', '').strip()
    resultats = {}
    total = 0

    if query:
        khassidas = Khassida.objects.filter(titre__icontains=query)
        corans = Coran.objects.filter(titre__icontains=query)
        zikrs = Zikr.objects.filter(titre__icontains=query)
        wirds = Wird.objects.filter(titre__icontains=query)
        sons = Son.objects.filter(titre__icontains=query)

        resultats = {
            'Khassida': {'items': khassidas, 'icon': 'fa-book-open', 'url_name': 'lire_pdf', 'categorie': 'khassida'},
            'Coran': {'items': corans, 'icon': 'fa-quran', 'url_name': 'lire_pdf', 'categorie': 'coran'},
            'Zikr': {'items': zikrs, 'icon': 'fa-hands-praying', 'url_name': 'zikr_compteur', 'categorie': 'zikr'},
            'Wird': {'items': wirds, 'icon': 'fa-scroll', 'url_name': 'liste', 'categorie': 'wird'},
            'Son': {'items': sons, 'icon': 'fa-music', 'url_name': 'liste_sons', 'categorie': 'son'},
        }
        total = sum(r['items'].count() for r in resultats.values())

    return render(request, 'bibliotheque/recherche.html', {
        'query': query,
        'resultats': resultats,
        'total': total,
    })


# --- KHASSIDA EN PDF INTEGRATION ---

def khassida_external(request):
    """Vue pour afficher les Khassidas depuis khassidaenpdf.net en iframe intégré."""
    return render(request, 'bibliotheque/khassida_external.html')


# --- TABLEAU DE BORD SPIRITUEL ---

@login_required
def dashboard(request):
    """Tableau de bord personnel avec statistiques spirituelles."""
    from datetime import timedelta, date
    from django.db.models import Sum, Count
    from django.db.models.functions import TruncDate

    user = request.user

    # ── Totaux globaux ──
    total_grains = HistoriqueZikr.objects.filter(user=user).aggregate(
        total=Sum('nombre_total'))['total'] or 0

    total_seances = HistoriqueZikr.objects.filter(user=user).count()

    total_lectures = ProgressionLecture.objects.filter(user=user).count()

    # ── Progression hebdomadaire (7 derniers jours) ──
    today = date.today()
    week_start = today - timedelta(days=6)
    week_data_qs = (
        HistoriqueZikr.objects
        .filter(user=user, date_seance__date__gte=week_start)
        .annotate(jour=TruncDate('date_seance'))
        .values('jour')
        .annotate(total=Sum('nombre_total'))
        .order_by('jour')
    )
    # Construire un dict jour → total pour les 7 derniers jours
    week_map = {entry['jour']: entry['total'] for entry in week_data_qs}
    week_labels = []
    week_values = []
    jours_fr = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
    for i in range(7):
        d = week_start + timedelta(days=i)
        week_labels.append(jours_fr[d.weekday()])
        week_values.append(week_map.get(d, 0))

    # ── Streak (jours consécutifs) ──
    streak = 0
    check_day = today
    while True:
        has_seance = HistoriqueZikr.objects.filter(
            user=user, date_seance__date=check_day).exists()
        if has_seance:
            streak += 1
            check_day -= timedelta(days=1)
        else:
            break

    # ── Top 3 Zikrs les plus récités ──
    top_zikrs = (
        HistoriqueZikr.objects
        .filter(user=user)
        .values('zikr__titre')
        .annotate(total=Sum('nombre_total'))
        .order_by('-total')[:3]
    )

    # ── Zikr d'aujourd'hui ──
    grains_today = HistoriqueZikr.objects.filter(
        user=user, date_seance__date=today
    ).aggregate(total=Sum('nombre_total'))['total'] or 0

    context = {
        'total_grains': total_grains,
        'total_seances': total_seances,
        'total_lectures': total_lectures,
        'streak': streak,
        'grains_today': grains_today,
        'week_labels': week_labels,
        'week_values': week_values,
        'week_max': max(week_values) if week_values else 1,
        'top_zikrs': top_zikrs,
    }
    return render(request, 'bibliotheque/dashboard.html', context)


# ── ZIKR COMMUNAUTAIRE ──

from django.db.models import Q

def zikr_communaute_list(request):
    # Toutes les sessions publiques actives (y compris avec formule de Zikr personnalisée)
    sessions = SessionZikrCommunautaire.objects.filter(
        est_actif=True,
        est_prive=False
    ).order_by('-date_debut')

    mes_sessions = []
    if request.user.is_authenticated:
        mes_sessions = SessionZikrCommunautaire.objects.filter(
            Q(createur=request.user) | Q(participations__utilisateur=request.user)
        ).distinct().order_by('-est_actif', '-date_debut')

    return render(request, 'bibliotheque/zikr_communaute_list.html', {
        'sessions': sessions,
        'mes_sessions': mes_sessions
    })

@login_required
def zikr_communaute_create(request):
    _ensure_default_zikrs()
    if request.method == 'POST':
        titre = (request.POST.get('titre') or '').strip()
        zikr_id = request.POST.get('zikr_id')
        zikr_personnalise = (request.POST.get('zikr_personnalise') or '').strip()
        try:
            objectif = max(1, int(request.POST.get('objectif_global', 1000)))
        except (ValueError, TypeError):
            objectif = 1000
        est_prive = request.POST.get('est_prive') == 'on'

        if titre and (zikr_id or zikr_personnalise):
            zikr = None
            if zikr_personnalise:
                # Créer ou récupérer aussi le Zikr dans la bibliothèque pour qu'il soit réutilisable
                zikr, _ = Zikr.objects.get_or_create(
                    titre=zikr_personnalise[:190],
                    defaults={'objectif_par_defaut': objectif}
                )
            elif zikr_id:
                zikr = get_object_or_404(Zikr, id=zikr_id)

            SessionZikrCommunautaire.objects.create(
                titre=titre,
                zikr=zikr,
                zikr_personnalise=zikr_personnalise,
                objectif_global=objectif,
                createur=request.user,
                est_prive=est_prive
            )
            return redirect('zikr_communaute_list')

    zikrs = Zikr.objects.all().order_by('id')
    return render(request, 'bibliotheque/zikr_communaute_create.html', {'zikrs': zikrs})

def zikr_communaute_detail(request, id):
    session = get_object_or_404(SessionZikrCommunautaire, id=id)
    
    if session.est_prive:
        code = request.GET.get('code')
        if code != session.code_partage and session.createur != request.user:
            has_participated = request.user.is_authenticated and session.participations.filter(utilisateur=request.user).exists()
            if not has_participated:
                return redirect('zikr_communaute_list')

    # Récupérer les top 50 participants
    classement = session.participations.all()[:50]
    
    ma_participation = None
    if request.user.is_authenticated:
        ma_participation, _ = ParticipationZikrCommunautaire.objects.get_or_create(
            session=session, 
            utilisateur=request.user
        )
        
    return render(request, 'bibliotheque/zikr_communaute_detail.html', {
        'session': session,
        'classement': classement,
        'ma_participation': ma_participation
    })

@login_required
def zikr_communaute_delete(request, id):
    session = get_object_or_404(SessionZikrCommunautaire, id=id)
    # Seul le créateur peut supprimer
    if session.createur == request.user:
        session.delete()
    return redirect('zikr_communaute_list')

@require_POST
def api_zikr_communaute_add(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Non connecté'}, status=403)
        
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        count_to_add = int(data.get('count', 1))
        
        session = SessionZikrCommunautaire.objects.get(id=session_id)
        if not session.est_actif:
            return JsonResponse({'status': 'error', 'message': 'Session terminée'})
            
        remaining = session.objectif_global - session.compteur_actuel
        if remaining <= 0:
            return JsonResponse({'status': 'error', 'message': 'Session terminée'})
            
        actual_count_to_add = min(count_to_add, remaining)
        
        # Mise à jour globale
        session.compteur_actuel += actual_count_to_add
        
        # Vérification si l'objectif est atteint
        if session.compteur_actuel >= session.objectif_global:
            session.est_actif = False
            
        session.save(update_fields=['compteur_actuel', 'est_actif'])
        
        # Mise à jour personnelle
        participation, _ = ParticipationZikrCommunautaire.objects.get_or_create(
            session=session,
            utilisateur=request.user
        )
        participation.contribution += actual_count_to_add
        participation.save(update_fields=['contribution', 'date_derniere_contribution'])
        
        return JsonResponse({
            'status': 'success',
            'global_count': session.compteur_actuel,
            'personal_count': participation.contribution,
            'is_completed': not session.est_actif
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# ── KAAMIL BI (Khatm du Coran) ──

def kaamil_list(request):
    sessions = SessionKaamil.objects.filter(
        est_actif=True,
        est_prive=False
    ).order_by('-date_debut')

    mes_sessions = []
    if request.user.is_authenticated:
        mes_sessions = SessionKaamil.objects.filter(
            Q(createur=request.user) | Q(jukkis__utilisateur=request.user)
        ).distinct().order_by('-est_actif', '-date_debut')

    return render(request, 'bibliotheque/kaamil_list.html', {
        'sessions': sessions,
        'mes_sessions': mes_sessions
    })

@login_required
def kaamil_create(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        est_prive = request.POST.get('est_prive') == 'on'
        
        if titre:
            SessionKaamil.objects.create(
                titre=titre,
                createur=request.user,
                est_prive=est_prive
            )
            return redirect('kaamil_list')
    
    return render(request, 'bibliotheque/kaamil_create.html')

def kaamil_detail(request, id):
    session = get_object_or_404(SessionKaamil, id=id)
    
    if session.est_prive:
        code = request.GET.get('code')
        if code != session.code_partage and session.createur != request.user:
            has_participated = request.user.is_authenticated and session.jukkis.filter(utilisateur=request.user).exists()
            if not has_participated:
                return redirect('kaamil_list')

    jukkis = session.jukkis.all().order_by('numero')
    
    # Calculs pour la barre de progression
    total_jukkis = 30
    jukkis_termines = jukkis.filter(est_termine=True).count()
    jukkis_pris = jukkis.filter(utilisateur__isnull=False).count()
    
    return render(request, 'bibliotheque/kaamil_detail.html', {
        'session': session,
        'jukkis': jukkis,
        'jukkis_termines': jukkis_termines,
        'jukkis_pris': jukkis_pris,
        'total_jukkis': total_jukkis
    })

@login_required
def kaamil_delete(request, id):
    session = get_object_or_404(SessionKaamil, id=id)
    if session.createur == request.user:
        session.delete()
    return redirect('kaamil_list')

@require_POST
def kaamil_prendre_jukki(request, jukki_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Non connecté'}, status=403)
        
    jukki = get_object_or_404(JukkiKaamil, id=jukki_id)
    
    if jukki.utilisateur is not None:
        return JsonResponse({'status': 'error', 'message': 'Ce Jukki est déjà pris'})
        
    jukki.utilisateur = request.user
    from django.utils import timezone
    jukki.date_prise = timezone.now()
    jukki.save()
    
    return JsonResponse({'status': 'success', 'message': f'Vous avez pris le Jukki {jukki.numero}'})

@require_POST
def kaamil_terminer_jukki(request, jukki_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Non connecté'}, status=403)
        
    jukki = get_object_or_404(JukkiKaamil, id=jukki_id)
    
    if jukki.utilisateur != request.user:
        return JsonResponse({'status': 'error', 'message': "Vous n'avez pas pris ce Jukki"})
        
    jukki.est_termine = True
    from django.utils import timezone
    jukki.date_fin = timezone.now()
    jukki.save()
    
    # Vérifier si toute la session est terminée
    if not jukki.session.jukkis.filter(est_termine=False).exists():
        jukki.session.est_actif = False
        jukki.session.save()
        
    return JsonResponse({'status': 'success', 'message': f'Jukki {jukki.numero} terminé !'})

@require_POST
def kaamil_liberer_jukki(request, jukki_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Non connecté'}, status=403)
        
    jukki = get_object_or_404(JukkiKaamil, id=jukki_id)
    
    if jukki.utilisateur != request.user and jukki.session.createur != request.user:
        return JsonResponse({'status': 'error', 'message': "Non autorisé"})
        
    jukki.utilisateur = None
    jukki.est_termine = False
    jukki.date_prise = None
    jukki.date_fin = None
    jukki.save()
    
    # Réactiver la session au cas où
    if not jukki.session.est_actif:
        jukki.session.est_actif = True
        jukki.session.save()
        
    return JsonResponse({'status': 'success'})

def kaamil_lire_jukki(request, jukki_id):
    jukki = get_object_or_404(JukkiKaamil, id=jukki_id)
    # The actual quran content fetching is done via JS in the template using the Al Quran Cloud API
    return render(request, 'bibliotheque/kaamil_lire.html', {
        'jukki': jukki
    })

# ── MODE HORS-LIGNE & NOTIFICATIONS INTELLIGENTES ──

def offline_view(request):
    """Page de secours hors-ligne intégrée au Service Worker PWA."""
    return render(request, 'bibliotheque/offline.html')


def notifications_list(request):
    """Centre de notifications & réglages horaires personnalisés (Prières, Verset, Citation, Khassidas, Coach Duolingo)."""
    notifications = []
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-date_creation')[:50]
    return render(request, 'bibliotheque/notifications.html', {
        'notifications': notifications
    })


def api_notifications_sync_feed(request):
    """Flux léger JSON pour les notifications locales programmées (nouveau Khassida, verset, citation, prières, streak Tazawwud)."""
    import datetime as dt
    feed_pub = cache.get('sdm_notif_pub_feed_v3')
    if feed_pub is None:
        latest_kh = Khassida.objects.only('id', 'titre').order_by('-id').first()
        latest_kh_data = {'id': latest_kh.id, 'titre': latest_kh.titre} if latest_kh else None

        latest_son = Son.objects.only('id', 'titre', 'auteur_voix').order_by('-id').first()
        latest_son_data = {
            'id': latest_son.id,
            'titre': latest_son.titre,
            'auteur': latest_son.auteur_voix or 'Kourel Mouride',
        } if latest_son else None

        wird_obj = Wird.objects.filter(titre__icontains='Mahuz').first() or Wird.objects.first()
        wird_url = f"/wird/{wird_obj.slug}/" if (wird_obj and wird_obj.slug) else "/collection/wird/"

        # Extraits Khassidas disponibles comme sons de notification / prière
        alert_sounds = [
            {
                'id': 'wajahtou_ht',
                'label': 'Wajahtou Wadjhiyaza · Hizbut Tarqiyyah',
                'url': 'https://res.cloudinary.com/dcajqzg2h/video/upload/v1795376309/media/audios/telegram/khassida/KURELSQACIDAS_8012_Wajahtou_Wadjhiyaza.mp3',
            },
        ]
        for s_item in Son.objects.filter(categorie__in=['KHASSIDA', 'ADHAN']).exclude(lien_audio_externe='').only('id', 'titre', 'auteur_voix', 'lien_audio_externe')[:8]:
            if s_item.lien_audio_externe and s_item.lien_audio_externe.startswith('http'):
                alert_sounds.append({
                    'id': f'son_{s_item.id}',
                    'label': f"{(s_item.titre or 'Khassida')[:38]} · {(s_item.auteur_voix or 'SDM')[:20]}",
                    'url': s_item.lien_audio_externe,
                })

        # Citation du jour (depuis nos citations vérifiées SDM & Masaalikul Jinaan)
        citation_data = {
            'id': 'mj_v1089',
            'texte': "La meilleure parure dont l'homme puisse se parer est la bonne conduite (al-adab) partout où il passe.",
            'source': "Masaalikul Jinaan · Cheikh Ahmadou Bamba (RTA)",
            'badge': "Masaalikul Jinaan"
        }
        rappels_path = os.path.join(settings.BASE_DIR, 'daily_rappels_sdm.json')
        if os.path.isfile(rappels_path):
            try:
                with open(rappels_path, 'r', encoding='utf-8') as rf:
                    cits = json.load(rf)
                if cits:
                    c = cits[dt.date.today().toordinal() % len(cits)]
                    oeuvre = c.get('oeuvre') or c.get('badge') or 'Masaalikul Jinaan'
                    auteur = c.get('auteur') or 'Cheikh Ahmadou Bamba (RTA)'
                    citation_data = {
                        'id': c.get('id') or 'mj_v1089',
                        'texte': (c.get('texte') or '')[:220],
                        'source': f"{oeuvre} · {auteur}",
                        'badge': c.get('badge') or 'Citation SDM',
                    }
            except Exception:
                pass

        # Verset du jour
        verset_data = {
            'ar': 'أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ',
            'fr': "N'est-ce point par l'évocation d'Allah que se tranquillisent les cœurs ?",
            'ref': "Sourate Ar-Ra'd (13:28)"
        }
        cnt_jour = ContenuDuJour.objects.order_by('id')
        if cnt_jour.exists():
            raw_c = cnt_jour[dt.date.today().timetuple().tm_yday % cnt_jour.count()]
            parts = (raw_c.verset_du_jour or '').split('\n— ')
            ref = parts[1] if len(parts) > 1 else 'Saint Coran'
            subs = parts[0].split('\n\n')
            verset_data = {
                'ar': subs[0] if len(subs) > 1 else '',
                'fr': subs[1] if len(subs) > 1 else subs[0],
                'ref': ref,
            }

        # Horaires de prière (ParametresPriere ou Dakar par défaut)
        prayers = [
            {'name': 'Fajr (Subh)', 'time': '05:45'},
            {'name': 'Tisbar (Dhuhr)', 'time': '13:15'},
            {'name': 'Takussan (Asr)', 'time': '16:35'},
            {'name': 'Timiss (Maghrib)', 'time': '18:55'},
            {'name': 'Guéwé (Isha)', 'time': '20:05'},
        ]
        cfg = ParametresPriere.objects.first()
        if cfg:
            def _fmt_t(val, fb):
                try:
                    return val.strftime('%H:%M') if val else fb
                except Exception:
                    return str(val)[:5] if val else fb
            prayers = [
                {'name': 'Fajr (Subh)', 'time': _fmt_t(getattr(cfg, 'fajr', None), '05:45')},
                {'name': 'Tisbar (Dhuhr)', 'time': _fmt_t(getattr(cfg, 'tisbar', None), '13:15')},
                {'name': 'Takussan (Asr)', 'time': _fmt_t(getattr(cfg, 'takussan', None), '16:35')},
                {'name': 'Timiss (Maghrib)', 'time': _fmt_t(getattr(cfg, 'timiss', None), '18:55')},
                {'name': 'Guéwé (Isha)', 'time': _fmt_t(getattr(cfg, 'guewe', None), '20:05')},
            ]

        feed_pub = {
            'latest_khassida': latest_kh_data,
            'latest_son': latest_son_data,
            'wird_url': wird_url,
            'alert_sounds': alert_sounds,
            'citation_du_jour': citation_data,
            'verset_du_jour': verset_data,
            'prayers': prayers,
        }
        cache.set('sdm_notif_pub_feed_v3', feed_pub, 180)

    # État Tazawwud "Mode Duolingo" personnel
    tazawwud_state = {'done_today': False, 'missed_yesterday': False, 'streak': 0, 'score_total': 0}
    if request.user.is_authenticated:
        try:
            from .models import TazawwudProgression, TazawwudReponseHistorique
            prog = TazawwudProgression.objects.filter(user=request.user).first()
            today_d = timezone.now().date()
            yest_d = today_d - datetime.timedelta(days=1)
            done_today = TazawwudReponseHistorique.objects.filter(user=request.user, date_tentative__date=today_d).exists()
            done_yest = TazawwudReponseHistorique.objects.filter(user=request.user, date_tentative__date=yest_d).exists()
            has_any = TazawwudReponseHistorique.objects.filter(user=request.user).exists()
            tazawwud_state = {
                'done_today': done_today,
                'missed_yesterday': (has_any and not done_yest and not done_today),
                'streak': prog.serie_jours if prog else 0,
                'score_total': prog.score_total if prog else 0,
            }
        except Exception:
            pass

    return JsonResponse({**feed_pub, 'tazawwud': tazawwud_state})

@login_required
@require_POST
def mark_notifications_read(request):
    """Marque toutes les notifications non lues comme lues."""
    Notification.objects.filter(user=request.user, est_lue=False).update(est_lue=True)
    return JsonResponse({"status": "success"})

@login_required
@require_POST
def update_notif_pref(request):
    """Mise à jour des préférences de notification."""
    try:
        data = json.loads(request.body)
        pref = data.get('pref')
        value = data.get('value')
        
        if pref in ['notif_prieres', 'notif_wird', 'notif_nouveau_contenu']:
            setattr(request.user.profile, pref, value)
            request.user.profile.save()
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error", "message": "Préférence invalide"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

@login_required
@require_POST
def update_location(request):
    """Mise à jour de la localisation de l'utilisateur pour l'Adhan."""
    try:
        data = json.loads(request.body)
        lat = data.get('latitude')
        lng = data.get('longitude')
        tz = data.get('timezone')
        if lat is not None and lng is not None:
            request.user.profile.latitude = float(lat)
            request.user.profile.longitude = float(lng)
            if tz:
                request.user.profile.fuseau_horaire = tz
            request.user.profile.save(update_fields=['latitude', 'longitude', 'fuseau_horaire'])
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Données manquantes'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# ── QUIZZ ISLAMIQUE (2 000+ QUESTIONS ALÉATOIRES & DÉFI MULTIJOUEUR LIVE) ──
from django.db.models import Sum
from django.urls import reverse
from .models import CategorieQuiz, NiveauQuiz, Question, Choix, ScoreJoueur, DefiMultijoueur, ParticipationDefi
from .quiz_bank import sample_quiz_questions, get_quiz_bank_stats, QUIZ_THEMES


def _get_player_identity(request):
    """Identifie le joueur (utilisateur connecté OU ami invité par prénom dans la salle de défi)."""
    if request.user.is_authenticated:
        return f"u:{request.user.id}", request.user.username
    guest = (request.session.get('sdm_guest_name') or '').strip()
    gid = request.session.get('sdm_guest_id')
    if not gid:
        import uuid
        gid = uuid.uuid4().hex[:8]
        request.session['sdm_guest_id'] = gid
    return f"g:{gid}", guest


def _get_lobby_state(code):
    key = f"sdm_defi_lobby_{code.upper()}"
    state = cache.get(key)
    if not state:
        state = {'players': {}, 'started_at': None, 'theme': 'mixte', 'round': 1}
    return key, state


def quiz_home(request):
    score = None
    defis_recents = []
    if request.user.is_authenticated:
        score, _ = ScoreJoueur.objects.get_or_create(utilisateur=request.user)
        score.verifier_niveau()
        defis_recents = ParticipationDefi.objects.filter(utilisateur=request.user).select_related('defi', 'defi__niveau_choisi').order_by('-date_participation')[:6]
    else:
        class _GuestScore:
            points_totaux = int(request.session.get('sdm_guest_quiz_pts', 0))
            niveau_actuel = None
        score = _GuestScore()

    niveaux = NiveauQuiz.objects.all().order_by('numero')
    total_bank_q, theme_counts = get_quiz_bank_stats()
    themes_cards = []
    for t in QUIZ_THEMES:
        cnt = total_bank_q if t['slug'] == 'mixte' else theme_counts.get(t['slug'], 0)
        themes_cards.append({**t, 'count': cnt})

    context = {
        'score': score,
        'niveaux': niveaux,
        'themes_cards': themes_cards,
        'total_bank_q': total_bank_q,
        'defis_recents': defis_recents,
    }
    return render(request, 'bibliotheque/quiz/quiz_home.html', context)


@login_required(login_url='/login/')
def quiz_play_random(request, theme_slug='mixte'):
    """Lance une manche aléatoire de 10 questions uniques (sans répétition) depuis la banque massive."""
    diff_param = request.GET.get('diff')
    diff = int(diff_param) if diff_param in ('1', '2', '3') else None
    seen = request.session.get('sdm_quiz_seen_ids', [])
    if len(seen) > 400:
        seen = seen[-150:]

    questions_data = sample_quiz_questions(theme_slug=theme_slug, difficulty=diff, count=10, exclude_ids=seen)
    seen.extend([q['id'] for q in questions_data])
    request.session['sdm_quiz_seen_ids'] = seen

    theme_meta = next((t for t in QUIZ_THEMES if t['slug'] == theme_slug), QUIZ_THEMES[0])
    total_bank_q, _ = get_quiz_bank_stats()
    return render(request, 'bibliotheque/quiz/quiz_play.html', {
        'theme': {'nom': theme_meta['nom'], 'slug': theme_slug},
        'total_bank_q': total_bank_q,
        'questions_json': json.dumps(questions_data, ensure_ascii=False),
        'replay_url': request.get_full_path(),
    })


@login_required(login_url='/login/')
def quiz_play(request, niveau_id):
    niveau = get_object_or_404(NiveauQuiz, id=niveau_id)
    if request.user.is_authenticated:
        score, _ = ScoreJoueur.objects.get_or_create(utilisateur=request.user)
        if score.points_totaux < niveau.points_requis:
            messages.error(request, "Vous n'avez pas assez de points pour débloquer ce niveau.")
            return redirect('quiz_home')

    diff = min(3, max(1, int(getattr(niveau, 'numero', 1) or 1)))
    seen = request.session.get('sdm_quiz_seen_ids', [])
    questions_data = sample_quiz_questions(theme_slug='mixte', difficulty=diff, count=10, exclude_ids=seen)
    seen.extend([q['id'] for q in questions_data])
    request.session['sdm_quiz_seen_ids'] = seen[-400:]

    total_bank_q, _ = get_quiz_bank_stats()
    return render(request, 'bibliotheque/quiz/quiz_play.html', {
        'niveau': niveau,
        'total_bank_q': total_bank_q,
        'questions_json': json.dumps(questions_data, ensure_ascii=False),
        'replay_url': request.get_full_path(),
    })


@login_required(login_url='/login/')
def quiz_play_theme(request, categorie_id):
    categorie = get_object_or_404(CategorieQuiz, id=categorie_id)
    cn = (categorie.nom or '').lower()
    slug = 'mouridisme' if 'mourid' in cn else ('coran' if 'coran' in cn else ('prophetes' if 'proph' in cn else 'fiqh'))
    return redirect('quiz_play_random', theme_slug=slug)


@csrf_exempt
def api_quiz_save_score(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            points_gagnes = int(data.get('score', 0))
            if request.user.is_authenticated:
                score, _ = ScoreJoueur.objects.get_or_create(utilisateur=request.user)
                score.points_totaux += points_gagnes
                score.verifier_niveau()
                return JsonResponse({'status': 'success', 'nouveau_total': score.points_totaux})
            cur = int(request.session.get('sdm_guest_quiz_pts', 0)) + points_gagnes
            request.session['sdm_guest_quiz_pts'] = cur
            return JsonResponse({'status': 'success', 'nouveau_total': cur})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=400)


def quiz_result(request, score, total):
    return render(request, 'bibliotheque/quiz/quiz_result.html', {'score': score, 'total': total})


def defi_create(request):
    """Crée une salle de Défi Multijoueur en temps réel avec code partagé et questions identiques."""
    niveaux = NiveauQuiz.objects.all().order_by('numero')
    if request.method == 'POST':
        niveau_id = request.POST.get('niveau_id')
        theme_slug = (request.POST.get('theme_slug') or 'mixte').strip()
        guest_name = (request.POST.get('guest_name') or '').strip()
        if not request.user.is_authenticated:
            if guest_name:
                request.session['sdm_guest_name'] = guest_name[:28]
            elif not request.session.get('sdm_guest_name'):
                request.session['sdm_guest_name'] = 'Joueur SDM'
        niveau = NiveauQuiz.objects.filter(id=niveau_id).first() or niveaux.first()
        if not niveau:
            niveau, _ = NiveauQuiz.objects.get_or_create(numero=1, defaults={'nom': 'Débutant', 'points_requis': 0})

        from django.contrib.auth.models import User as AuthUser
        creator = request.user if request.user.is_authenticated else (AuthUser.objects.filter(is_superuser=True).first() or AuthUser.objects.first())
        defi = DefiMultijoueur.objects.create(createur=creator, niveau_choisi=niveau)
        key, lobby = _get_lobby_state(defi.code_partage)
        lobby['theme'] = theme_slug
        pid, pname = _get_player_identity(request)
        lobby['host_pid'] = pid
        lobby['players'][pid] = {
            'name': pname or 'Créateur',
            'status': 'PRET',
            'score': 0,
            'q_num': 0,
            'seen_at': timezone.now().timestamp(),
        }
        cache.set(key, lobby, 3600)
        return redirect('defi_detail', code=defi.code_partage)

    return render(request, 'bibliotheque/quiz/defi_create.html', {
        'niveaux': niveaux,
        'themes_cards': QUIZ_THEMES,
    })


def defi_join_by_code(request):
    """Permet à un ami de rejoindre directement une salle en saisissant son code de défi."""
    code = (request.POST.get('code') or request.GET.get('code') or '').strip().upper()
    if not code:
        messages.error(request, "Veuillez saisir le code du défi de votre ami.")
        return redirect('quiz_home')
    defi = DefiMultijoueur.objects.filter(code_partage__iexact=code).first()
    if not defi:
        messages.error(request, f"Aucun défi trouvé avec le code « {code} ». Vérifiez le code envoyé par votre ami.")
        return redirect('quiz_home')
    return redirect('defi_detail', code=defi.code_partage)


def defi_detail(request, code):
    """Salle d'attente & classement EN DIRECT : les deux amis se voient instantanément sans perdre le lien."""
    defi = get_object_or_404(DefiMultijoueur, code_partage__iexact=code)

    # Permettre à l'ami invité d'entrer son prénom en 1 clic sans redirection bloquante vers /login/
    if request.method == 'POST' and request.POST.get('guest_name'):
        request.session['sdm_guest_name'] = request.POST.get('guest_name').strip()[:28]
        return redirect('defi_detail', code=defi.code_partage)

    pid, pname = _get_player_identity(request)
    needs_name = (not request.user.is_authenticated and not pname)

    key, lobby = _get_lobby_state(defi.code_partage)
    if not needs_name:
        existing = lobby['players'].get(pid, {})
        lobby['players'][pid] = {
            'name': pname,
            'status': existing.get('status') or 'PRET',
            'score': existing.get('score', 0),
            'q_num': existing.get('q_num', 0),
            'seen_at': timezone.now().timestamp(),
        }
        cache.set(key, lobby, 3600)

    participations = defi.participations.select_related('utilisateur').all().order_by('-score')
    a_deja_joue = (request.user.is_authenticated and participations.filter(utilisateur=request.user).exists()) or (
        lobby['players'].get(pid, {}).get('status') == 'TERMINE'
    )
    est_hote = (lobby.get('host_pid') == pid) or (request.user.is_authenticated and defi.createur_id == request.user.id)

    share_url = request.build_absolute_uri(reverse('defi_detail', args=[defi.code_partage]))
    whatsapp_text = f"⚡ Je te défie au Quizz Islamique SDM ! Rejoins ma salle (Code : {defi.code_partage}) ici : {share_url}"
    theme_meta = next((t for t in QUIZ_THEMES if t['slug'] == lobby.get('theme', 'mixte')), QUIZ_THEMES[0])

    return render(request, 'bibliotheque/quiz/defi_detail.html', {
        'defi': defi,
        'participations': participations,
        'a_deja_joue': a_deja_joue,
        'est_hote': est_hote,
        'needs_name': needs_name,
        'player_name': pname,
        'player_pid': pid,
        'share_url': share_url,
        'whatsapp_text': whatsapp_text,
        'theme_nom': theme_meta['nom'],
    })


@csrf_exempt
def api_defi_lobby(request, code):
    """Synchronisation temps réel (toutes les 2,5s) de la salle de défi entre amis : présence, lancement synchronisé & scores."""
    defi = get_object_or_404(DefiMultijoueur, code_partage__iexact=code)
    pid, pname = _get_player_identity(request)
    key, lobby = _get_lobby_state(defi.code_partage)
    now_ts = timezone.now().timestamp()

    if request.method == 'POST':
        try:
            body = json.loads(request.body or '{}')
        except Exception:
            body = {}
        action = body.get('action', 'ping')
        if pname:
            cur = lobby['players'].get(pid, {'name': pname, 'status': 'PRET', 'score': 0, 'q_num': 0})
            cur['name'] = pname
            cur['seen_at'] = now_ts
            if action == 'progress':
                cur['status'] = 'EN_COURS'
                cur['score'] = int(body.get('score', cur.get('score', 0)))
                cur['q_num'] = int(body.get('q_num', cur.get('q_num', 0)))
            elif action == 'finish':
                cur['status'] = 'TERMINE'
                cur['score'] = int(body.get('score', cur.get('score', 0)))
                cur['q_num'] = 10
            elif action == 'start_all':
                lobby['started_at'] = now_ts
                cur['status'] = 'EN_COURS'
            elif action == 'new_round':
                lobby['round'] = int(lobby.get('round', 1)) + 1
                lobby['started_at'] = now_ts
                for p in lobby['players'].values():
                    p['status'] = 'PRET'
                    p['score'] = 0
                    p['q_num'] = 0
            lobby['players'][pid] = cur
            cache.set(key, lobby, 3600)

    # Construire la liste unifiée (joueurs live dans la salle + participations DB)
    players_out = []
    seen_names = set()
    for p_id, info in lobby['players'].items():
        online = (now_ts - info.get('seen_at', 0)) < 25
        players_out.append({
            'pid': p_id,
            'name': info.get('name', 'Joueur'),
            'status': info.get('status', 'PRET'),
            'score': int(info.get('score', 0)),
            'q_num': int(info.get('q_num', 0)),
            'online': online,
            'is_me': (p_id == pid),
        })
        seen_names.add(info.get('name', '').lower())

    for part in defi.participations.select_related('utilisateur').all().order_by('-score'):
        uname = part.utilisateur.username
        if uname.lower() not in seen_names:
            players_out.append({
                'pid': f'u:{part.utilisateur_id}',
                'name': uname,
                'status': 'TERMINE',
                'score': part.score,
                'q_num': 10,
                'online': False,
                'is_me': (request.user.is_authenticated and part.utilisateur_id == request.user.id),
            })

    players_out.sort(key=lambda x: (-x['score'], not x['online'], x['name'].lower()))
    return JsonResponse({
        'code': defi.code_partage,
        'started_at': lobby.get('started_at'),
        'round': lobby.get('round', 1),
        'players': players_out,
        'online_count': sum(1 for p in players_out if p['online']),
    })


def defi_play(request, code):
    """Lance exactement les MÊMES 10 questions aléatoires pour tous les amis de la salle."""
    defi = get_object_or_404(DefiMultijoueur, code_partage__iexact=code)
    pid, pname = _get_player_identity(request)
    if not pname:
        return redirect('defi_detail', code=defi.code_partage)

    key, lobby = _get_lobby_state(defi.code_partage)
    theme_slug = lobby.get('theme', 'mixte')
    round_num = int(lobby.get('round', 1))
    diff = min(3, max(1, int(getattr(defi.niveau_choisi, 'numero', 1) or 1))) if defi.niveau_choisi else None

    # Tirage DÉTERMINISTE par code + numéro de manche -> TOUS les amis ont exactement les mêmes questions !
    questions_data = sample_quiz_questions(
        theme_slug=theme_slug,
        difficulty=diff,
        count=10,
        seed=f"sdm_defi_{defi.code_partage}_r{round_num}",
    )

    lobby['players'][pid] = {
        'name': pname,
        'status': 'EN_COURS',
        'score': 0,
        'q_num': 1,
        'seen_at': timezone.now().timestamp(),
    }
    cache.set(key, lobby, 3600)

    return render(request, 'bibliotheque/quiz/defi_play.html', {
        'defi': defi,
        'player_name': pname,
        'round_num': round_num,
        'questions_json': json.dumps(questions_data, ensure_ascii=False),
    })


@csrf_exempt
def api_defi_save_score(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            points_gagnes = int(data.get('score', 0))
            code = (data.get('code') or '').strip().upper()
            defi = get_object_or_404(DefiMultijoueur, code_partage__iexact=code)
            pid, pname = _get_player_identity(request)

            key, lobby = _get_lobby_state(defi.code_partage)
            lobby['players'][pid] = {
                'name': pname or 'Joueur SDM',
                'status': 'TERMINE',
                'score': points_gagnes,
                'q_num': 10,
                'seen_at': timezone.now().timestamp(),
            }
            cache.set(key, lobby, 3600)

            if request.user.is_authenticated:
                part, created = ParticipationDefi.objects.get_or_create(
                    defi=defi, utilisateur=request.user, defaults={'score': points_gagnes}
                )
                if not created and points_gagnes > part.score:
                    part.score = points_gagnes
                    part.save(update_fields=['score'])

                score_joueur, _ = ScoreJoueur.objects.get_or_create(utilisateur=request.user)
                score_joueur.points_totaux += points_gagnes
                score_joueur.verifier_niveau()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

# ── TAZAWWUDU-Ç-ÇIGHÂR VIEWS (importé de tazawwud_views) ──
from .tazawwud_views import (
    tazawwud_home, tazawwud_dashboard, tazawwud_module, tazawwud_lecon,
    tazawwud_quiz, tazawwud_revision, tazawwud_entrainement,
    tazawwud_recharger_vies, api_tazawwud_reponse, api_tazawwud_save_score,
    tazawwud_initier_paiement, tazawwud_paiement_callback, tazawwud_paiement_webhook,
    tazawwud_paiement_simulation, tazawwud_compagnons, api_tazawwud_ajouter_compagnon,
    api_tazawwud_repondre_compagnon, tazawwud_toggle_visibilite, tazawwud_classement_hebdo,
    tazawwud_creer_defi, tazawwud_jouer_defi
)
