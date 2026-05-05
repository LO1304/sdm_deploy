from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Khassida, Coran, Zikr, Wird, EtapeWird, Son, Profile, Favori, ContenuDuJour

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'user', 'est_premium', 'date_expiration', 'type_soutien']

class KhassidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Khassida
        fields = '__all__'

class CoranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coran
        fields = '__all__'

class ZikrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zikr
        fields = '__all__'

class EtapeWirdSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtapeWird
        fields = '__all__'

class WirdSerializer(serializers.ModelSerializer):
    etapes = EtapeWirdSerializer(many=True, read_only=True)
    class Meta:
        model = Wird
        fields = '__all__'

class SonSerializer(serializers.ModelSerializer):
    categorie_display = serializers.CharField(source='get_categorie_display', read_only=True)
    class Meta:
        model = Son
        fields = '__all__'

class ContenuDuJourSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContenuDuJour
        fields = '__all__'

class FavoriSerializer(serializers.ModelSerializer):
    content_type_model = serializers.CharField(source='content_type.model', read_only=True)
    
    class Meta:
        model = Favori
        fields = ['id', 'object_id', 'content_type_model', 'date_ajout']
