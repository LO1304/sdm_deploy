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


# --- VUES PRINCIPALES ---

def home(request):
    """Page d'accueil avec horaires de prières et contenus récents."""
    import datetime
    
    # Automatisation du contenu du jour : rotation quotidienne
    tous_les_contenus = ContenuDuJour.objects.order_by('id')
    contenu = None
    if tous_les_contenus.exists():
        jour_annee = datetime.date.today().timetuple().tm_yday
        count = tous_les_contenus.count()
        if count > 0:
            index = jour_annee % count
            raw_contenu = tous_les_contenus[index]
            
            # Helper pour parser les textes avec "\n\n" et "\n— "
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
    khassida = Khassida.objects.all()
    zikrs = Zikr.objects.all()
    recents_khassidas = Khassida.objects.order_by('-id')[:6]

    config = ParametresPriere.objects.first()
    
    # Données réservées aux utilisateurs connectés
    derniere_lecture = None
    dernier_son = None
    wird_mahuz = None
    wird_en_cours = None
    total_zikr_user = 0
    niveau_spirituel = 1
    total_ecoutes = 0
    
    if request.user.is_authenticated:
        # Récupérer la dernière lecture pour le bouton "Reprendre"
        derniere_progression = ProgressionLecture.objects.filter(user=request.user).order_by('-derniere_mise_a_jour').first()
        if derniere_progression and derniere_progression.content_object:
            derniere_lecture = {
                'obj': derniere_progression.content_object,
                'page': derniere_progression.page_actuelle,
                'categorie': 'coran' if isinstance(derniere_progression.content_object, Coran) else 'khassida'
            }

        # Récupérer le dernier son écouté depuis l'historique
        try:
            son_ct = ContentType.objects.get_for_model(Son)
            dernier_historique_son = Historique.objects.filter(user=request.user, content_type=son_ct).order_by('-date_lecture').first()
            dernier_son = dernier_historique_son.content_object if dernier_historique_son else None
        except Exception:
            dernier_son = None
            
        # --- NOUVEAUTÉS DASHBOARD MOBILE ---
        # 1. Total Zikr
        zikr_aggr = HistoriqueZikr.objects.filter(user=request.user).aggregate(total=Sum('nombre_total'))
        total_zikr_user = zikr_aggr['total'] or 0
        
        # 2. Wird Mahuz
        wird_mahuz = Wird.objects.filter(titre__icontains='Mahuz').first()
        # Vérifier si l'utilisateur a un Wird en cours (via ProgressionWird qui garde l'état courant)
        wird_en_cours = ProgressionWird.objects.filter(user=request.user).order_by('-derniere_modif').first()
        
        # 3. Calcul du niveau spirituel (Basé sur les interactions : Zikr + Ecoutes + Lectures)
        total_ecoutes = Historique.objects.filter(user=request.user).count()
        points = (total_zikr_user // 100) + total_ecoutes
        niveau_spirituel = 1 + (points // 50)  # Niveau 1 par défaut, augmente tous les 50 "points"

    # Nombre de contenus pour les badges
    total_khassidas = Khassida.objects.count()
    total_corans = Coran.objects.count()
    total_sons = Son.objects.count()
    total_zikrs = Zikr.objects.count()

    context = {
        'contenu': contenu,
        'khassidas': khassida,
        'recents': recents_khassidas,
        'zikrs': zikrs,
        'config': config,
        'derniere_lecture': derniere_lecture,
        'dernier_son': dernier_son,
        'wird_mahuz': wird_mahuz,
        'wird_en_cours': wird_en_cours,
        'total_zikr_user': total_zikr_user,
        'niveau_spirituel': niveau_spirituel,
        'total_ecoutes': total_ecoutes,
        'total_khassidas': total_khassidas,
        'total_corans': total_corans,
        'total_sons': total_sons,
        'total_zikrs': total_zikrs,
    }
    return render(request, 'bibliotheque/index.html', context)

def liste_dynamique(request, categorie):
    """Affiche les listes filtrées par catégorie (Khassida, Coran, etc.)."""
    query = request.GET.get('search')
    template_name = 'bibliotheque/liste.html'
    items = []

    if categorie == 'khassida':
        items = Khassida.objects.all()
    elif categorie == 'zikr':
        return redirect('zikr_compteur_default')
    elif categorie == 'wird':
        items = Wird.objects.all()
    elif categorie == 'coran':
        items = Coran.objects.all()
        return render(request, 'bibliotheque/coran_interactif.html', {
            'coran_pdfs': items,
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

    # Fetch all sounds for background audio player
    sons = Son.objects.all().order_by('-date_ajout')

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
    """Liste audio filtrable."""
    categorie_filter = request.GET.get('cat')
    if categorie_filter:
        sons = Son.objects.filter(categorie=categorie_filter).order_by('-date_ajout')
    else:
        sons = Son.objects.all().order_by('-date_ajout')
    
    categories = Son.CATEGORIES
    
    # Get favorited sound IDs for the current user
    favoris_ids = []
    if request.user.is_authenticated:
        try:
            son_ct = ContentType.objects.get_for_model(Son)
            favoris_ids = list(Favori.objects.filter(user=request.user, content_type=son_ct).values_list('object_id', flat=True))
        except Exception:
            pass

    return render(request, 'bibliotheque/liste_sons.html', {
        'sons': sons,
        'categories': categories,
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
                clean_name = re.sub(r'[_\-]+', ' ', raw_name).strip()
                track_title = titre_saisi if (titre_saisi and len(fichiers) == 1) else (
                    f"{titre_saisi} ({idx + 1})" if titre_saisi else (clean_name or "Son Telegram")
                )

                upload_res = cloudinary.uploader.upload(
                    f,
                    resource_type='video',
                    folder='media/audios/telegram',
                    use_filename=True,
                    unique_filename=True,
                )
                secure_url = upload_res.get('secure_url')
                if not secure_url:
                    continue

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
    """Page de profil utilisateur avec statistiques spirituelles complètes."""
    profile, created = Profile.objects.get_or_create(user=request.user)

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

@login_required
def toggle_favori(request, model_name, object_id):
    from django.apps import apps
    try:
        model_class = apps.get_model('bibliotheque', model_name)
    except LookupError:
        return JsonResponse({'status': 'error'})
    
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
        
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': status})
    
    # Redirect to the previous page
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

    context = {
        'telechargements_by_type': telechargements_by_type
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

# ── NOTIFICATIONS ──

@login_required
def notifications_list(request):
    """Affiche la liste des notifications de l'utilisateur."""
    notifications = Notification.objects.filter(user=request.user).order_by('-date_creation')
    return render(request, 'bibliotheque/notifications.html', {
        'notifications': notifications
    })

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


# ── QUIZZ ISLAMIQUE ──
from django.db.models import Sum
from .models import CategorieQuiz, NiveauQuiz, Question, Choix, ScoreJoueur, DefiMultijoueur, ParticipationDefi
import json

@login_required(login_url='login')
def quiz_home(request):
    score, _ = ScoreJoueur.objects.get_or_create(utilisateur=request.user)
    score.verifier_niveau()
    niveaux = NiveauQuiz.objects.all().order_by('numero')
    categories = CategorieQuiz.objects.all()
    
    context = {
        'score': score,
        'niveaux': niveaux,
        'categories': categories,
        'defis_recents': ParticipationDefi.objects.filter(utilisateur=request.user).order_by('-date_participation')[:5]
    }
    return render(request, 'bibliotheque/quiz/quiz_home.html', context)

@login_required(login_url='login')
def quiz_play(request, niveau_id):
    niveau = get_object_or_404(NiveauQuiz, id=niveau_id)
    score = ScoreJoueur.objects.get(utilisateur=request.user)
    
    if score.points_totaux < niveau.points_requis:
        messages.error(request, "Vous n'avez pas assez de points pour débloquer ce niveau.")
        return redirect('quiz_home')
        
    questions = list(niveau.questions.all())
    import random
    random.shuffle(questions)
    # On prend max 10 questions pour la partie
    questions = questions[:10]
    
    questions_data = []
    for q in questions:
        choix = list(q.choix.all())
        random.shuffle(choix)
        questions_data.append({
            'id': q.id,
            'texte': q.texte,
            'points': q.points,
            'choix': [{'id': c.id, 'texte': c.texte, 'est_correct': c.est_correct} for c in choix]
        })
        
    context = {
        'niveau': niveau,
        'questions_json': json.dumps(questions_data)
    }
    return render(request, 'bibliotheque/quiz/quiz_play.html', context)

@login_required(login_url='login')
def quiz_play_theme(request, categorie_id):
    categorie = get_object_or_404(CategorieQuiz, id=categorie_id)
    
    questions = list(categorie.questions.all())
    import random
    random.shuffle(questions)
    questions = questions[:10]
    
    questions_data = []
    for q in questions:
        choix = list(q.choix.all())
        random.shuffle(choix)
        questions_data.append({
            'id': q.id,
            'texte': q.texte,
            'points': q.points,
            'explication': q.explication,
            'choix': [{'id': c.id, 'texte': c.texte, 'est_correct': c.est_correct} for c in choix]
        })
        
    context = {
        'theme': categorie,
        'questions_json': json.dumps(questions_data)
    }
    return render(request, 'bibliotheque/quiz/quiz_play.html', context)

@csrf_exempt
@login_required
def api_quiz_save_score(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            points_gagnes = int(data.get('score', 0))
            score, _ = ScoreJoueur.objects.get_or_create(utilisateur=request.user)
            score.points_totaux += points_gagnes
            score.verifier_niveau()
            return JsonResponse({'status': 'success', 'nouveau_total': score.points_totaux})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def quiz_result(request, score, total):
    return render(request, 'bibliotheque/quiz/quiz_result.html', {'score': score, 'total': total})

@login_required
def defi_create(request):
    if request.method == 'POST':
        niveau_id = request.POST.get('niveau_id')
        niveau = get_object_or_404(NiveauQuiz, id=niveau_id)
        defi = DefiMultijoueur.objects.create(createur=request.user, niveau_choisi=niveau)
        return redirect('defi_detail', code=defi.code_partage)
        
    niveaux = NiveauQuiz.objects.all().order_by('numero')
    return render(request, 'bibliotheque/quiz/defi_create.html', {'niveaux': niveaux})

@login_required
def defi_detail(request, code):
    defi = get_object_or_404(DefiMultijoueur, code_partage=code)
    participations = defi.participations.all().order_by('-score')
    
    a_deja_joue = participations.filter(utilisateur=request.user).exists()
    
    # URL de partage WhatsApp
    share_url = request.build_absolute_import_url(f"/quiz/defi/{code}/") if hasattr(request, 'build_absolute_import_url') else request.build_absolute_uri()
    whatsapp_text = f"Viens me défier au Quizz Islamique ! Clique ici : {share_url}"
    
    return render(request, 'bibliotheque/quiz/defi_detail.html', {
        'defi': defi, 
        'participations': participations,
        'a_deja_joue': a_deja_joue,
        'whatsapp_text': whatsapp_text
    })

@login_required
def defi_play(request, code):
    defi = get_object_or_404(DefiMultijoueur, code_partage=code)
    
    if ParticipationDefi.objects.filter(defi=defi, utilisateur=request.user).exists():
        messages.error(request, "Vous avez déjà participé à ce défi.")
        return redirect('defi_detail', code=code)
        
    questions = list(defi.niveau_choisi.questions.all())
    import random
    random.shuffle(questions)
    questions = questions[:10]
    
    questions_data = []
    for q in questions:
        choix = list(q.choix.all())
        random.shuffle(choix)
        questions_data.append({
            'id': q.id,
            'texte': q.texte,
            'points': q.points,
            'choix': [{'id': c.id, 'texte': c.texte, 'est_correct': c.est_correct} for c in choix]
        })
        
    return render(request, 'bibliotheque/quiz/defi_play.html', {
        'defi': defi,
        'questions_json': json.dumps(questions_data)
    })

@csrf_exempt
@login_required
def api_defi_save_score(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            points_gagnes = int(data.get('score', 0))
            code = data.get('code')
            
            defi = get_object_or_404(DefiMultijoueur, code_partage=code)
            ParticipationDefi.objects.get_or_create(defi=defi, utilisateur=request.user, defaults={'score': points_gagnes})
            
            # Update global score too
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
