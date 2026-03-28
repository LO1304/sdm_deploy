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
    Khassida, Zikr, Wird, ContenuDuJour, Coran, 
    ParametresPriere, Historique, HistoriqueZikr, 
    Son, Profile, HistoriqueConsultation, Favori, ProgressionLecture
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

    context = {
        'contenu': contenu,
        'khassidas': khassida,
        'recents': recents_khassidas,
        'zikrs': zikrs,
        'config': config,
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
        
    document = get_object_or_404(target_model, id=id)
    
    # Récupérer la progression
    page_reprise = 1
    content_type = ContentType.objects.get_for_model(target_model)
    prog = ProgressionLecture.objects.filter(user=request.user, content_type=content_type, object_id=id).first()
    if prog:
        page_reprise = prog.page_actuelle

    return render(request, 'bibliotheque/lecteur.html', {
        'document': document,
        'categorie': categorie,
        'page_reprise': page_reprise
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
