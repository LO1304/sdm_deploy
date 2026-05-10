from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from bibliotheque import views # Vérifie bien le nom de ton app ici

urlpatterns = [
    # PWA et Offline
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/javascript'), name='sw.js'),
    path('offline/', TemplateView.as_view(template_name='bibliotheque/offline.html'), name='offline'),

    # Accueil et Authentification
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='bibliotheque/login.html'), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Profil et Abonnement
    path('profile/', views.profil_view, name='profile'),
    path('abonnement/', views.page_abonnement, name='abonnement'),
    path('paiement-confirmation/', views.paiement_reussi, name='paiement_reussi'),
    path('wird/<slug:slug>/', views.lire_wird, name='lire_wird'),
    path('api/wird/save-progress/', views.save_wird_progress, name='save_wird_progress'),
    path('favoris/', views.view_favoris, name='favoris'),
    path('favoris/toggle/<str:model_name>/<int:object_id>/', views.toggle_favori, name='toggle_favori'),

    # Contenu (Sons, Coran, etc.)
    path('collection/son/', views.liste_sons, name='liste_sons'),
    path('collection/<str:categorie>/', views.liste_dynamique, name='liste'),
    path('lire/<str:categorie>/<int:id>/', views.lire_pdf, name='lire_pdf'),
    path('proxy-pdf/<str:categorie>/<int:id>/', views.proxy_pdf, name='proxy_pdf'),
    path('zikr-compteur/<int:id>/', views.zikr_compteur, name='zikr_compteur'),
    path('voir-historique/', views.voir_historique, name='voir_historique'),
    path('historique/zikr/', views.voir_historique_zikr, name='voir_historique_zikr'),
    path('historique/general/', views.voir_historique_general, name='voir_historique_general'),
    path('details/<int:id>/', views.details_contenu, name='details_contenu'),
    path('api/enregistrer-seance/', views.enregistrer_seance, name='enregistrer_seance'),
    path('api/ecoute-son/<int:id>/', views.enregistrer_ecoute_son, name='enregistrer_ecoute_son'),
    path('api/progression-pdf/', views.sauvegarder_progression_pdf, name='sauvegarder_progression_pdf'),
    
    # Recherche globale
    path('recherche/', views.recherche_globale, name='recherche_globale'),

    # Tableau de bord personnel
    path('dashboard/', views.dashboard, name='dashboard'),
]

# Gestion des fichiers média et statiques en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)