from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# ── KHASSIDA ──
class Khassida(models.Model):
    titre = models.CharField(max_length=255, db_index=True)
    auteur = models.CharField(max_length=255, default="Cheikh Ahmadou Bamba")
    fichier_pdf = models.FileField(upload_to='khassidas/')
    image_couverture = models.ImageField(upload_to='couvertures/', blank=True, null=True)

    def __str__(self):
        return self.titre


# ── CORAN ──
class Coran(models.Model):
    titre = models.CharField(max_length=100, db_index=True)
    numero = models.IntegerField(blank=True, null=True)
    traduction_fr = models.TextField(blank=True, null=True)
    fichier_pdf = models.FileField(upload_to='coran_pdf/', blank=True, null=True)
    fichier_audio = models.FileField(upload_to='coran_audio/', blank=True, null=True)

    def __str__(self):
        return self.titre


# ── ZIKR ──
class Zikr(models.Model):
    titre = models.CharField(max_length=200, db_index=True)
    texte_arabe = models.TextField(blank=True)
    transcription = models.TextField(blank=True)
    traduction = models.TextField(blank=True)
    objectif_par_defaut = models.PositiveIntegerField(default=33)
    fichier_audio = models.FileField(upload_to='zikrs_audio/', blank=True, null=True)

    def __str__(self):
        return self.titre

# ── ZIKR COMMUNAUTAIRE ──
class SessionZikrCommunautaire(models.Model):
    titre = models.CharField(max_length=200, help_text="Ex: Grand Zikr du Vendredi")
    zikr = models.ForeignKey(Zikr, on_delete=models.CASCADE, related_name='sessions_communautaires')
    objectif_global = models.PositiveIntegerField(default=100000, help_text="Objectif total à atteindre par la communauté")
    compteur_actuel = models.PositiveIntegerField(default=0, help_text="Progression actuelle")
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions_creees')
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(blank=True, null=True)
    est_actif = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_debut']

    def __str__(self):
        return self.titre

class ParticipationZikrCommunautaire(models.Model):
    session = models.ForeignKey(SessionZikrCommunautaire, on_delete=models.CASCADE, related_name='participations')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations_zikr')
    contribution = models.PositiveIntegerField(default=0)
    date_derniere_contribution = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('session', 'utilisateur')
        ordering = ['-contribution', 'date_derniere_contribution']

    def __str__(self):
        return f"{self.utilisateur.username} - {self.contribution} sur {self.session.titre}"

# ── HISTORIQUE ──
class Historique(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historiques')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date_lecture = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_lecture']

    def __str__(self):
        return f"{self.user.username} a écouté {self.content_object} le {self.date_lecture}"


# ── PROGRESSION LECTURE ──
class ProgressionLecture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progressions')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    page_actuelle = models.PositiveIntegerField(default=1)
    derniere_mise_a_jour = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self):
        return f"{self.user.username} - {self.content_object} (Page {self.page_actuelle})"


# ── WIRD ──
class Wird(models.Model):
    titre = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, db_index=True)
    auteur = models.CharField(max_length=255, default="Cheikh Ahmadou Bamba")
    introduction = models.TextField()
    description_courte = models.TextField(blank=True, help_text="Résumé pour la liste")
    image_couverture = models.ImageField(upload_to='wirds/', blank=True, null=True)
    transcription = models.TextField(blank=True, help_text="Transcription")
    traduction = models.TextField(blank=True, help_text="Traduction")
    nombre_repetitions = models.IntegerField(default=100)
    fichier_audio = models.FileField(upload_to='audios/wird', blank=True, null=True)

    def __str__(self):
        return self.titre


class EtapeWird(models.Model):
    TYPES = [
        ('prep', 'Préparation'), ('protec', 'Protection'), ('invoc', 'Invocation'),
        ('istighfar', 'Istighfar'), ('shahada', 'Shahada'), ('salawat', 'Salawat'),
        ('tawheed', 'Tawheed'), ('cloture', 'Clôture'), ('quranic', 'Quranique')
    ]
    wird = models.ForeignKey(Wird, on_delete=models.CASCADE, related_name='etapes')
    numero = models.PositiveIntegerField()
    titre_arabe = models.CharField(max_length=255)
    titre_francais = models.CharField(max_length=255)
    texte_arabe = models.TextField()
    transliteration = models.TextField(blank=True)
    traduction_francais = models.TextField(blank=True)
    repetitions = models.PositiveIntegerField(default=1)
    duree_estimee = models.PositiveIntegerField(default=1, help_text="Minutes")
    notes_spirituelles = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=TYPES, default='invoc')
    conseil_spirituel = models.TextField(blank=True)
    fichier_audio = models.FileField(upload_to='audios/etapes/', blank=True, null=True)

    class Meta:
        ordering = ['numero']
        unique_together = ('wird', 'numero')

    def __str__(self):
        return f"{self.wird.titre} - Etape {self.numero}: {self.titre_francais}"


# ── CONTENU DU JOUR ──
class ContenuDuJour(models.Model):
    verset_du_jour = models.TextField(help_text="Verset en arabe et en français")
    beuyit_du_jour = models.TextField(help_text="vers de khassida")
    rappel_dujour = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Contenu du jour pour {self.date}"


# ── PARAMÈTRES PRIÈRE ──
class ParametresPriere(models.Model):
    ville = models.CharField(max_length=100, default="Touba")
    activer_adhan = models.BooleanField(default=True)
    fichier_adhan = models.FileField(upload_to='audios/adhan', blank=True, null=True)
    rappel_avant_priere = models.IntegerField(help_text="Minutes avant l'heure de la prière", default=15)

    def __str__(self):
        return f"Paramètres pour {self.ville}"


# ── PROFIL UTILISATEUR ──
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    est_premium = models.BooleanField(default=False)
    date_expiration = models.DateField(null=True, blank=True)
    type_soutien = models.CharField(max_length=20, choices=[('DON', 'Don'), ('ABO', 'Abonnement')], null=True)
    fcm_token = models.CharField(max_length=255, blank=True, null=True, help_text="Jeton Firebase Cloud Messaging pour les notifications push")

    def __str__(self):
        return f"Profil de {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)


# ── SONS / AUDIO ──
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

    titre = models.CharField(max_length=200, db_index=True)
    auteur_voix = models.CharField(max_length=150, blank=True, null=True, help_text="Nom du Kourel, du conférencier ou du Rajass")
    categorie = models.CharField(max_length=20, choices=CATEGORIES, default='KHASSIDA', db_index=True)
    fichier_audio = models.FileField(
        upload_to='sons/',
        blank=True,
        null=True
    )
    lien_audio_externe = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Lien Cloudinary ou externe (prioritaire sur le fichier local)"
    )
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} ({self.get_categorie_display()})"

    class Meta:
        verbose_name = "Son"
        verbose_name_plural = "Sons"
        ordering = ['-date_ajout']


# ── HISTORIQUE ZIKR ──
class HistoriqueZikr(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    zikr = models.ForeignKey(Zikr, on_delete=models.CASCADE)
    nombre_total = models.PositiveIntegerField()
    date_seance = models.DateTimeField(auto_now_add=True)


# ── PROGRESSION GÉNÉRALE ──
class ProgressionGenerale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    derniere_lecture = models.DateTimeField(auto_now=True)
    termine = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Progression Générale"


# ── HISTORIQUE CONSULTATION ──
class HistoriqueConsultation(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    categorie = models.CharField(max_length=50)
    date_vue = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} a lu {self.titre} ({self.date_vue})"


# ── FAVORIS ──
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


# ── TELECHARGEMENTS ──
class Telechargement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='telechargements')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date_telechargement = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_telechargement']
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self):
        return f"{self.user.username} a téléchargé {self.content_object}"



# ── HISTORIQUE WIRD ──
class HistoriqueWird(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wird = models.ForeignKey(Wird, on_delete=models.CASCADE)
    etape_max = models.PositiveIntegerField(default=1)
    complete = models.BooleanField(default=False)
    temps_total = models.DurationField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    derniere_activite = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.wird.titre} ({'Fini' if self.complete else 'En cours'})"


# ── PROGRESSION WIRD ──
class ProgressionWird(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wird = models.ForeignKey(Wird, on_delete=models.CASCADE)
    etape_courante = models.PositiveIntegerField(default=1)
    repetitions_faites = models.PositiveIntegerField(default=0)
    temps_ecoule = models.DurationField(null=True, blank=True)
    derniere_modif = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'wird')
