from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User



# Create your models here.

class Khassida(models.Model):
    titre = models.CharField(max_length=255)
    auteur= models.CharField(max_length=255,default="Cheikh Ahmadou Bamba ")
    fichier_pdf = models.FileField(upload_to='khassidas/')
    image_couverture=models.ImageField(upload_to='couvertures/',blank=True,null=True)

    def __str__(self):
        return self.titre

class Coran(models.Model):
    titre = models.CharField(max_length=100)
    # On met blank=True et null=True pour que ce ne soit plus obligatoire
    numero = models.IntegerField(blank=True, null=True) 
    traduction_fr = models.TextField(blank=True, null=True)
    # ON AJOUTE LE PDF ICI
    fichier_pdf = models.FileField(upload_to='coran_pdf/', blank=True, null=True)
    fichier_audio = models.FileField(upload_to='coran_audio/', blank=True, null=True)

    def __str__(self):
        return self.titre
    
class Zikr(models.Model):
    titre = models.CharField(max_length=200)
    texte_arabe = models.TextField(blank=True) # Le texte en Arabe
    transcription = models.TextField(blank=True) # Le texte en phonétique
    traduction = models.TextField(blank=True) # Le sens en Français
    objectif_par_defaut = models.PositiveIntegerField(default=33)
    fichier_audio = models.FileField(upload_to='zikrs_audio/', blank=True, null=True)

    def __str__(self):
        return self.titre

#Historique 

class Historique(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historiques')
    # On utilise GenericForeignKey pour pouvoir lier l'historique 
    # à n'importe quel modèle (Coran, Khassida, ou Son)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    date_lecture = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_lecture'] # Le plus récent en haut

    def __str__(self):
        return f"{self.user.username} a écouté {self.content_object} le {self.date_lecture}"
#wird
class Wird(models.Model):
    titre=models.CharField(max_length=200)
    introduction=models.TextField()
    transcription=models.TextField(help_text="Transcription")
    traduction=models.TextField(help_text="Traduction")
    nombre_repetitions=models.IntegerField(default=100)
    fichier_audio = models.FileField(upload_to='audios/wird',blank=True,null=True)
    
    def __str__(self):
        return self.titre
    

#Contenu du jour 
class ContenuDuJour(models.Model):
    verset_du_jour=models.TextField(help_text="Verset en arabe et en français")
    beuyit_du_jour=models.TextField(help_text="vers de khassida")
    rappel_dujour=models.TextField()
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"""Contenu du jour pour {self.date}"""
    
#Prayer 
class ParametresPriere(models.Model):
    ville = models.CharField(max_length=100, default="Touba")
    activer_adhan = models.BooleanField(default=True)
    fichier_adhan=models.FileField(upload_to='audios/adhan',blank=True,null=True)
    rappel_avant_priere = models.IntegerField(help_text="Minutes avant l'heure de la prière", default=15)
    

    def __str__(self):
        return f"Paramètres pour {self.ville}"
    

from django.db import models
from cloudinary_storage.storage import VideoMediaCloudinaryStorage  # Ajoute cet import en haut

# 1. Fonction pour organiser les fichiers dans les dossiers media
#def upload_path(instance, filename):
    # Range le fichier dans media/audios/NOM_CATEGORIE/nom_du_fichier
    #return f'audios/{instance.categorie.lower()}/{filename}'

# 2. Modèle unique pour gérer tous les sons (plus simple pour ton code)
class Son(models.Model):
    CATEGORIES = [
        ('CORAN', 'Coran'),
        ('KHASSIDA', 'Khassida'),
        ('ADHAN', 'Adhan'),
        ('WAKHTANE', 'Wakhtane'),
        ('XAM_XAM', 'Xam Xam'),
        ('ZIKR', 'Zikr'),
        ('RAJASS', 'Rajass'),
    ]

    titre = models.CharField(max_length=200)
    auteur_voix = models.CharField(
        max_length=150, 
        blank=True, 
        null=True, 
        help_text="Nom du Kourel, du conférencier ou du Rajass"
    )
    categorie = models.CharField(
        max_length=20, 
        choices=CATEGORIES, 
        default='KHASSIDA'
    )
    # Utilisation de la fonction dynamique pour le rangement
    # Remplace ta ligne actuelle par celle-ci :
    fichier_audio = models.FileField(upload_to='sons/', storage=VideoMediaCloudinaryStorage())
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} ({self.get_categorie_display()})"

    class Meta:
        verbose_name = "Son"
        verbose_name_plural = "Sons"
        ordering = ['-date_ajout']


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    est_premium = models.BooleanField(default=False)
    date_expiration = models.DateField(null=True, blank=True)
    type_soutien = models.CharField(max_length=20, choices=[('DON', 'Don'), ('ABO', 'Abonnement')], null=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

# Ce code crée automatiquement un profil quand un nouvel utilisateur s'inscrit
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

from django.contrib import messages
from django.shortcuts import redirect

def paiement_reussi(request):
    profile = request.user.profile
    profile.est_premium = True
    profile.save()
    
    # On envoie un message de succès
    messages.success(request, "Félicitations ! Votre accès Premium SDM est désormais actif. Profitez de votre musique sans pub !")
    
    return redirect('home')


class HistoriqueZikr(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Ajoute cette ligne si elle manque
    zikr = models.ForeignKey(Zikr, on_delete=models.CASCADE)
    nombre_total = models.PositiveIntegerField()
    date_seance = models.DateTimeField(auto_now_add=True)


from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class ProgressionGenerale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Permet de pointer vers n'importe quel modèle (Khassida, Coran, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    derniere_lecture = models.DateTimeField(auto_now=True)
    termine = models.BooleanField(default=False) # Pour savoir s'il a fini l'écoute/lecture

    class Meta:
        verbose_name = "Progression Générale"

class HistoriqueConsultation(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    categorie = models.CharField(max_length=50) # 'coran', 'khassida', etc.
    date_vue = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} a lu {self.titre} ({self.date_vue})"

class Favori(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoris')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_ajout']
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self):
        return f"{self.user.username} a ajouté {self.content_object} à ses favoris"
