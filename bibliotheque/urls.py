from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from bibliotheque import views, firebase_auth_view

urlpatterns = [
    # Accueil et Authentification
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('firebase-login/', firebase_auth_view.firebase_login, name='firebase_login'),

    # Profil et Abonnement
    path('profile/', views.profil_view, name='profile'),
    path('abonnement/', views.page_abonnement, name='abonnement'),
    path('paiement-confirmation/', views.paiement_reussi, name='paiement_reussi'),
    path('wird/<slug:slug>/', views.lire_wird, name='lire_wird'),
    path('api/wird/save-progress/', views.save_wird_progress, name='save_wird_progress'),
    path('favoris/', views.view_favoris, name='favoris'),
    path('favoris/toggle/<str:model_name>/<int:object_id>/', views.toggle_favori, name='toggle_favori'),
    path('telechargements/', views.view_telechargements, name='telechargements'),
    path('telechargements/ajouter/<str:model_name>/<int:object_id>/', views.ajouter_telechargement, name='ajouter_telechargement'),

    # Contenu (Sons, Coran, etc.)
    path('collection/son/', views.liste_sons, name='liste_sons'),
    path('collection/<str:categorie>/', views.liste_dynamique, name='liste'),
    path('lire/<str:categorie>/<int:id>/', views.lire_pdf, name='lire_pdf'),
    path('zikr-compteur/<int:id>/', views.zikr_compteur, name='zikr_compteur'),
    path('voir-historique/', views.voir_historique, name='voir_historique'),
    path('historique/zikr/', views.voir_historique_zikr, name='voir_historique_zikr'),
    path('historique/general/', views.voir_historique_general, name='voir_historique_general'),
    path('details/<int:id>/', views.details_contenu, name='details_contenu'),
    path('api/enregistrer-seance/', views.enregistrer_seance, name='enregistrer_seance'),
    path('api/ecoute-son/<int:id>/', views.enregistrer_ecoute_son, name='enregistrer_ecoute_son'),
    path('api/progression-pdf/', views.sauvegarder_progression_pdf, name='sauvegarder_progression_pdf'),

    # Proxy PDF pour contourner les problèmes CORS avec Cloudinary
    path('proxy-pdf/<str:categorie>/<int:id>/', views.proxy_pdf, name='proxy_pdf'),

    # Khassida externe
    path('khassida-externe/', views.khassida_external, name='khassida_external'),
    
    # Recherche globale
    path('recherche/', views.recherche_globale, name='recherche_globale'),

    # Tableau de bord personnel
    path('dashboard/', views.dashboard, name='dashboard'),
    # Zikr Communautaire
    path('communaute/zikr/', views.zikr_communaute_list, name='zikr_communaute_list'),
    path('communaute/zikr/creer/', views.zikr_communaute_create, name='zikr_communaute_create'),
    path('communaute/zikr/<int:id>/', views.zikr_communaute_detail, name='zikr_communaute_detail'),
    path('api/communaute/zikr/add/', views.api_zikr_communaute_add, name='api_zikr_communaute_add'),
    
    # Tâches quotidiennes (Cron Gratuit)
    path('api/trigger-daily-tasks/', views.trigger_daily_tasks, name='trigger_daily_tasks'),
]

# Gestion des fichiers média et statiques en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)