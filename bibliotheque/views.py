import os
import requests
import json
import hashlib
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
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
    SessionZikrCommunautaire, ParticipationZikrCommunautaire
)
from .forms import ModernRegisterForm

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
            contenu = tous_les_contenus[index]
    khassida = Khassida.objects.all()
    zikrs = Zikr.objects.all()
    recents_khassidas = Khassida.objects.order_by('-id')[:6]

    config = ParametresPriere.objects.first()
    
    # Données réservées aux utilisateurs connectés
    derniere_lecture = None
    dernier_son = None
    
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
        items = Zikr.objects.all()
    elif categorie == 'wird':
        items = Wird.objects.all()
    elif categorie == 'coran':
        items = Coran.objects.all()

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
    
    # Récupérer la progression
    page_reprise = 1
    if request.user.is_authenticated:
        content_type = ContentType.objects.get_for_model(target_model)
        prog = ProgressionLecture.objects.filter(user=request.user, content_type=content_type, object_id=id).first()
        if prog:
            page_reprise = prog.page_actuelle

    # Fetch all sounds for background audio player
    sons = Son.objects.all().order_by('-date_ajout')

    # Préparer l'URL directe du PDF comme fallback pour le JS
    direct_pdf_url = ''
    try:
        if document.fichier_pdf:
            raw_url = document.fichier_pdf.url
            if raw_url.startswith('//'):
                direct_pdf_url = 'https:' + raw_url
            elif raw_url.startswith('http'):
                direct_pdf_url = raw_url
            else:
                direct_pdf_url = raw_url  # URL relative locale
            
            # Si c'est une URL Cloudinary, utiliser l'API Admin pour la vraie URL
            if 'cloudinary' in direct_pdf_url or direct_pdf_url.startswith('http'):
                try:
                    import cloudinary
                    import cloudinary.api
                    from django.conf import settings as conf_settings
                    cloud_config = getattr(conf_settings, 'CLOUDINARY_STORAGE', {})
                    cloudinary.config(
                        cloud_name=cloud_config.get('CLOUD_NAME', ''),
                        api_key=cloud_config.get('API_KEY', ''),
                        api_secret=cloud_config.get('API_SECRET', ''),
                        secure=True,
                    )
                    resource_info = cloudinary.api.resource(
                        str(document.fichier_pdf),
                        resource_type='raw',
                        type='upload',
                    )
                    real_url = resource_info.get('secure_url', '')
                    if real_url:
                        direct_pdf_url = real_url
                except Exception:
                    pass  # Garder l'URL non signée comme fallback
    except (ValueError, Exception):
        direct_pdf_url = ''

    return render(request, 'bibliotheque/lecteur.html', {
        'document': document,
        'categorie': categorie,
        'page_reprise': page_reprise,
        'sons': sons,
        'direct_pdf_url': direct_pdf_url,
    })

def proxy_pdf(request, categorie, id):
    """Proxy robuste : streaming du PDF avec URLs signées Cloudinary."""
    import cloudinary
    import cloudinary.utils
    from django.conf import settings as conf_settings
    
    target_model = Coran if categorie == 'coran' else Khassida
    document = get_object_or_404(target_model, id=id)
    
    # Enregistrer automatiquement le téléchargement pour l'utilisateur
    if request.user.is_authenticated:
        try:
            content_type = ContentType.objects.get_for_model(target_model)
            Telechargement.objects.get_or_create(
                user=request.user,
                content_type=content_type,
                object_id=id
            )
        except Exception as e:
            print(f"[proxy_pdf] Erreur telechargement: {e}")
            
    # Récupérer l'URL du PDF
    try:
        if not document.fichier_pdf:
            return HttpResponse("Fichier PDF non disponible", status=404)
        pdf_url = document.fichier_pdf.url
        pdf_name = str(document.fichier_pdf)
    except (ValueError, Exception):
        return HttpResponse("Fichier PDF non disponible", status=404)
    
    # ── Fichier local : servir directement ──
    if pdf_url.startswith('/') and not pdf_url.startswith('//'):
        file_path = os.path.join(conf_settings.MEDIA_ROOT, pdf_name)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                res = HttpResponse(f.read(), content_type='application/pdf')
                res['Access-Control-Allow-Origin'] = '*'
                res['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
                res['Cache-Control'] = 'public, max-age=86400'
                filename = f"{document.titre.replace(' ', '_')}.pdf"
                res['Content-Disposition'] = f'inline; filename="{filename}"'
                return res
        return HttpResponse("Fichier local introuvable", status=404)
    
    # ── Fichier distant (Cloudinary) ──
    # Configurer Cloudinary
    cloud_config = getattr(conf_settings, 'CLOUDINARY_STORAGE', {})
    cloudinary.config(
        cloud_name=cloud_config.get('CLOUD_NAME', os.environ.get('CLOUDINARY_CLOUD_NAME', 'dcajqzg2h')),
        api_key=cloud_config.get('API_KEY', os.environ.get('CLOUDINARY_API_KEY', '')),
        api_secret=cloud_config.get('API_SECRET', os.environ.get('CLOUDINARY_API_SECRET', '')),
        secure=True,
    )
    
    # ── Solution Ultime : Contourner le blocage PDF de Cloudinary via ZIP ──
    # Cloudinary bloque la distribution des fichiers PDF "raw" par défaut (Erreur 401).
    # L'astuce consiste à demander à l'API de générer un ZIP contenant le PDF, 
    # de le télécharger, et de l'extraire en mémoire pour le servir au navigateur.
    try:
        import cloudinary.utils
        import zipfile
        import io
        
        print(f"[proxy_pdf] Generation URL ZIP pour: {pdf_name}")
        zip_url = cloudinary.utils.download_zip_url(
            public_ids=[pdf_name],
            resource_type='raw'
        )
        
        remote = requests.get(zip_url, timeout=30)
        
        if remote.status_code == 200:
            # Extraire le PDF depuis le ZIP en mémoire
            z = zipfile.ZipFile(io.BytesIO(remote.content))
            filename_in_zip = z.namelist()[0]
            pdf_data = z.read(filename_in_zip)
            
            print(f"[proxy_pdf] OK PDF extrait du ZIP ({len(pdf_data)} bytes)")
            res = HttpResponse(pdf_data, content_type='application/pdf')
            res['Access-Control-Allow-Origin'] = '*'
            res['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
            res['Cache-Control'] = 'public, max-age=86400'
            filename = f"{document.titre.replace(' ', '_')}.pdf"
            res['Content-Disposition'] = f'inline; filename="{filename}"'
            return res
        else:
            print(f"[proxy_pdf] WARN ZIP download failed: HTTP {remote.status_code}")
    except Exception as e:
        print(f"[proxy_pdf] WARN ZIP workaround failed: {e}")
        
    # Si le workaround ZIP échoue, on tente de récupérer la secure_url API comme dernier recours
    try:
        import cloudinary.api
        resource_info = cloudinary.api.resource(pdf_name, resource_type='raw', type='upload')
        real_url = resource_info.get('secure_url', '')
        if real_url:
            print(f"[proxy_pdf] TRY API secure_url: {real_url[:120]}")
            remote = requests.get(real_url, timeout=25, stream=True)
            if remote.status_code == 200 and len(remote.content) > 0:
                res = HttpResponse(remote.content, content_type='application/pdf')
                res['Access-Control-Allow-Origin'] = '*'
                res['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
                res['Cache-Control'] = 'public, max-age=86400'
                filename = f"{document.titre.replace(' ', '_')}.pdf"
                res['Content-Disposition'] = f'inline; filename="{filename}"'
                return res
    except Exception as e:
        print(f"[proxy_pdf] API fallback failed: {e}")
    
    # Toutes les tentatives ont échoué
    return HttpResponse(
        "Impossible de charger le PDF. Le fichier est restreint ou n'existe pas.", 
        status=502
    )

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

def zikr_compteur(request, id):
    """Interface du chapelet électronique."""
    zikr = get_object_or_404(Zikr, id=id)
    return render(request, 'bibliotheque/zikr_compteur.html', {'zikr': zikr})

@csrf_exempt
def enregistrer_seance(request):
    """API pour sauvegarder une séance de Zikr terminée."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            zikr_id = data.get('zikr_id')
            total = data.get('total')

            if not request.user.is_authenticated:
                return JsonResponse({'status': 'error', 'message': 'Connectez-vous pour enregistrer'}, status=403)

            zikr = get_object_or_404(Zikr, id=zikr_id)

            HistoriqueZikr.objects.create(
                user=request.user,
                zikr=zikr, 
                nombre_total=total
            )
            return JsonResponse({'status': 'success'})
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

# --- AUTHENTIFICATION & PROFIL ---

def login_view(request):
    """Vue de connexion sécurisée avec protection anti-brute-force."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Toujours rediriger vers l'accueil après connexion
            next_url = request.GET.get('next', 'home')
            if next_url == 'home' or not next_url:
                return redirect('home')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'bibliotheque/login.html', {'form': form})

def register_view(request):
    """Gestion de l'inscription utilisateur."""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = ModernRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Django nécessite de spécifier le backend s'il y en a plusieurs (ex: EmailAuthBackend + ModelBackend)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home') 
    else:
        form = ModernRegisterForm()
    return render(request, 'bibliotheque/register.html', {'form': form})

@login_required
def profil_view(request):
    """Vue du profil utilisateur avec statut Premium."""
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'bibliotheque/profile.html', {'profile': profile})

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

@login_required
def voir_historique(request):
    """Historique global du Zikr avec total des grains."""
    historique = HistoriqueZikr.objects.filter(user=request.user).order_by('-date_seance')
    total_grains = historique.aggregate(Sum('nombre_total'))['nombre_total__sum'] or 0
    return render(request, 'bibliotheque/historique.html', {
        'historique': historique,
        'total_grains': total_grains,
    })

@login_required
def voir_historique_zikr(request):
    historique = HistoriqueZikr.objects.filter(user=request.user).order_by('-date_seance')
    return render(request, 'bibliotheque/historique_zikr.html', {'historique': historique})

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


@login_required
def view_telechargements(request):
    telechargements = Telechargement.objects.filter(user=request.user)
    
    # Organiser les téléchargements par type
    telechargements_by_type = {
        'Khassida': [],
        'Coran': [],
        'Son': []
    }
    
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


@login_required
def ajouter_telechargement(request, model_name, object_id):
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

def zikr_communaute_list(request):
    sessions = SessionZikrCommunautaire.objects.filter(est_actif=True).order_by('-date_debut')
    return render(request, 'bibliotheque/zikr_communaute_list.html', {'sessions': sessions})

@login_required
def zikr_communaute_create(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        zikr_id = request.POST.get('zikr_id')
        objectif = int(request.POST.get('objectif_global', 100000))
        
        if titre and zikr_id:
            zikr = get_object_or_404(Zikr, id=zikr_id)
            SessionZikrCommunautaire.objects.create(
                titre=titre,
                zikr=zikr,
                objectif_global=objectif,
                createur=request.user
            )
            return redirect('zikr_communaute_list')
    
    zikrs = Zikr.objects.all()
    return render(request, 'bibliotheque/zikr_communaute_create.html', {'zikrs': zikrs})

def zikr_communaute_detail(request, id):
    session = get_object_or_404(SessionZikrCommunautaire, id=id)
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
            
        # Mise à jour globale
        session.compteur_actuel += count_to_add
        session.save(update_fields=['compteur_actuel'])
        
        # Mise à jour personnelle
        participation, _ = ParticipationZikrCommunautaire.objects.get_or_create(
            session=session,
            utilisateur=request.user
        )
        participation.contribution += count_to_add
        participation.save(update_fields=['contribution', 'date_derniere_contribution'])
        
        return JsonResponse({
            'status': 'success',
            'global_count': session.compteur_actuel,
            'personal_count': participation.contribution
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
