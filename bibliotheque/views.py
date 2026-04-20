import requests
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now

# Import de tes modèles
from .models import (
    Khassida, Coran, Zikr, Wird, EtapeWird, HistoriqueWird, ProgressionWird, Son, Profile, HistoriqueConsultation, Favori, ContenuDuJour, ParametresPriere, ProgressionLecture, Historique, HistoriqueZikr, ProgressionGenerale
)
from .forms import ModernRegisterForm

# --- VUES PRINCIPALES ---

def home(request):
    """Page d'accueil avec horaires de prières et contenus récents."""
    if not request.user.is_authenticated:
        return redirect('login')
    contenu = ContenuDuJour.objects.last()
    khassida = Khassida.objects.all()
    zikrs = Zikr.objects.all()
    recents_khassidas = Khassida.objects.order_by('-id')[:3] 

    config = ParametresPriere.objects.first()
    
    # Récupérer la dernière lecture pour le bouton "Reprendre"
    derniere_progression = ProgressionLecture.objects.filter(user=request.user).order_by('-derniere_mise_a_jour').first()
    derniere_lecture = None
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

    context = {
        'contenu': contenu,
        'khassidas': khassida,
        'recents': recents_khassidas,
        'zikrs': zikrs,
        'config': config,
        'derniere_lecture': derniere_lecture,
        'dernier_son': dernier_son,
    }
    return render(request, 'bibliotheque/index.html', context)

@login_required
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

@login_required
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
    content_type = ContentType.objects.get_for_model(target_model)
    prog = ProgressionLecture.objects.filter(user=request.user, content_type=content_type, object_id=id).first()
    if prog:
        page_reprise = prog.page_actuelle

    # Fetch all sounds for background audio player
    sons = Son.objects.all().order_by('-date_ajout')

    return render(request, 'bibliotheque/lecteur.html', {
        'document': document,
        'categorie': categorie,
        'page_reprise': page_reprise,
        'sons': sons
    })

@csrf_exempt
@login_required
def sauvegarder_progression_pdf(request):
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

@login_required
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

@login_required
def liste_sons(request):
    """Liste audio filtrable."""
    categorie_filter = request.GET.get('cat')
    if categorie_filter:
        sons = Son.objects.filter(categorie=categorie_filter).order_by('-date_ajout')
    else:
        sons = Son.objects.all().order_by('-date_ajout')
    
    categories = Son.CATEGORIES
    
    # Get favorited sound IDs for the current user
    try:
        son_ct = ContentType.objects.get_for_model(Son)
        favoris_ids = Favori.objects.filter(user=request.user, content_type=son_ct).values_list('object_id', flat=True)
    except Exception:
        favoris_ids = []

    return render(request, 'bibliotheque/liste_sons.html', {
        'sons': sons,
        'categories': categories,
        'active_cat': categorie_filter,
        'favoris_ids': list(favoris_ids),
    })

# --- AUTHENTIFICATION & PROFIL ---

def register_view(request):
    """Gestion de l'inscription utilisateur."""
    if request.method == 'POST':
        form = ModernRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
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

@login_required
def details_contenu(request, id):
    """Affiche les détails et enregistre la consultation dans l'historique."""
    contenu = get_object_or_404(Khassida, id=id)
    obj_type = ContentType.objects.get_for_model(contenu)
    Historique.objects.update_or_create(
        user=request.user,
        content_type=obj_type,
        object_id=contenu.id
    )
    return render(request, 'bibliotheque/details.html', {'contenu': contenu})

@csrf_exempt
@login_required
def enregistrer_ecoute_son(request, id):
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

@login_required
def lire_wird(request, slug):
    wird = get_object_or_404(Wird, slug=slug)
    etapes = wird.etapes.all().order_by('numero')
    
    progression, created = ProgressionWird.objects.get_or_create(
        user=request.user, 
        wird=wird
    )
    
    return render(request, 'bibliotheque/lire_wird.html', {
        'wird': wird,
        'etapes': etapes,
        'progression': progression,
    })

@login_required
def save_wird_progress(request):
    if request.method == 'POST':
        import json
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


# --- RECHERCHE GLOBALE ---

@login_required
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
