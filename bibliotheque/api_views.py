from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from .models import Khassida, Coran, Zikr, Wird, Son, Profile, Favori, ContenuDuJour
from .serializers import (
    UserSerializer, ProfileSerializer, KhassidaSerializer, CoranSerializer,
    ZikrSerializer, WirdSerializer, SonSerializer, FavoriSerializer, ContenuDuJourSerializer
)

class IsPremiumUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.est_premium

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    if not username or not password:
        return Response({'error': 'Veuillez fournir un nom d\'utilisateur et un mot de passe.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Ce nom d\'utilisateur existe déjà.'}, status=status.HTTP_400_BAD_REQUEST)
        
    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({'message': 'Utilisateur créé avec succès.'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)

class KhassidaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Khassida.objects.all()
    serializer_class = KhassidaSerializer
    permission_classes = [permissions.IsAuthenticated]

class CoranViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coran.objects.all()
    serializer_class = CoranSerializer
    permission_classes = [permissions.IsAuthenticated]

class ZikrViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Zikr.objects.all()
    serializer_class = ZikrSerializer
    permission_classes = [permissions.IsAuthenticated]

class WirdViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Wird.objects.all()
    serializer_class = WirdSerializer
    permission_classes = [permissions.IsAuthenticated]

class SonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Son.objects.all().order_by('-date_ajout')
    serializer_class = SonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        categorie = self.request.query_params.get('categorie', None)
        if categorie is not None:
            queryset = queryset.filter(categorie=categorie)
        return queryset

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_contenu_du_jour(request):
    contenu = ContenuDuJour.objects.last()
    if contenu:
        serializer = ContenuDuJourSerializer(contenu)
        return Response(serializer.data)
    return Response({'error': 'Aucun contenu trouvé'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def manage_favoris(request):
    if request.method == 'GET':
        favoris = Favori.objects.filter(user=request.user)
        serializer = FavoriSerializer(favoris, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        model_name = request.data.get('model_name')
        object_id = request.data.get('object_id')
        
        from django.apps import apps
        try:
            model_class = apps.get_model('bibliotheque', model_name)
        except LookupError:
            return Response({'error': 'Modèle introuvable'}, status=status.HTTP_400_BAD_REQUEST)
            
        content_type = ContentType.objects.get_for_model(model_class)
        favori, created = Favori.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id
        )
        if not created:
            favori.delete()
            return Response({'status': 'removed'})
        return Response({'status': 'added'}, status=status.HTTP_201_CREATED)
