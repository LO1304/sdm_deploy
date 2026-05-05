from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import api_views

router = DefaultRouter()
router.register(r'khassidas', api_views.KhassidaViewSet)
router.register(r'coran', api_views.CoranViewSet)
router.register(r'zikr', api_views.ZikrViewSet)
router.register(r'wirds', api_views.WirdViewSet)
router.register(r'sons', api_views.SonViewSet)

urlpatterns = [
    # Auth JWT
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', api_views.register_api, name='api_register'),
    
    # Profile & Content
    path('profile/', api_views.get_profile, name='api_profile'),
    path('contenu-du-jour/', api_views.get_contenu_du_jour, name='api_contenu_du_jour'),
    path('favoris/', api_views.manage_favoris, name='api_favoris'),
    
    # Routers pour les ViewSets
    path('', include(router.urls)),
]
