from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


# ── KHASSIDA ──
class Khassida(models.Model):
    titre = models.CharField(max_length=255, db_index=True)
    auteur = models.CharField(max_length=255, default="Cheikh Ahmadou Bamba")
    fichier_pdf = models.FileField(upload_to='khassidas/')
    image_couverture = models.ImageField(upload_to='couvertures/', blank=True, null=True)
    est_premium = models.BooleanField(default=False, help_text="Cocher pour réserver ce contenu aux utilisateurs Premium")

    def __str__(self):
        return self.titre


# ── CORAN ──
class Coran(models.Model):
    titre = models.CharField(max_length=100, db_index=True)
    numero = models.IntegerField(blank=True, null=True)
    traduction_fr = models.TextField(blank=True, null=True)
    fichier_pdf = models.FileField(upload_to='coran_pdf/', blank=True, null=True)
    fichier_audio = models.FileField(upload_to='coran_audio/', blank=True, null=True)
    est_premium = models.BooleanField(default=False, help_text="Cocher pour réserver ce contenu aux utilisateurs Premium")

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
    est_premium = models.BooleanField(default=False, help_text="Cocher pour réserver ce contenu aux utilisateurs Premium")

    def __str__(self):
        return self.titre

# ── ZIKR COMMUNAUTAIRE ──
class SessionZikrCommunautaire(models.Model):
    titre = models.CharField(max_length=200, help_text="Ex: Grand Zikr du Vendredi")
    zikr = models.ForeignKey(Zikr, on_delete=models.CASCADE, related_name='sessions_communautaires', null=True, blank=True)
    zikr_personnalise = models.TextField(blank=True, null=True, help_text="Formule personnalisée si aucun zikr prédéfini n'est choisi")
    objectif_global = models.PositiveIntegerField(default=100000, help_text="Objectif total à atteindre par la communauté")
    compteur_actuel = models.PositiveIntegerField(default=0, help_text="Progression actuelle")
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions_creees')
    est_prive = models.BooleanField(default=False)
    code_partage = models.CharField(max_length=50, blank=True, null=True, unique=True)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(blank=True, null=True)
    est_actif = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.est_prive and not self.code_partage:
            self.code_partage = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

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
        return f"{self.user.username} a écouté un(e) {self.content_type.model} (ID: {self.object_id}) le {self.date_lecture}"


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
    est_premium = models.BooleanField(default=False, help_text="Cocher pour réserver ce contenu aux utilisateurs Premium")

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
    latitude = models.FloatField(blank=True, null=True, help_text="Latitude pour le calcul des heures de prières")
    longitude = models.FloatField(blank=True, null=True, help_text="Longitude pour le calcul des heures de prières")
    fuseau_horaire = models.CharField(max_length=50, blank=True, null=True, help_text="Ex: Africa/Dakar")

    # Préférences de notifications
    notif_prieres = models.BooleanField(default=True, help_text="Recevoir les rappels de prière")
    notif_wird = models.BooleanField(default=True, help_text="Recevoir les rappels du wird quotidien")
    notif_nouveau_contenu = models.BooleanField(default=True, help_text="Être alerté des nouveaux Khassidas ou Audios")

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
    est_premium = models.BooleanField(default=False, help_text="Cocher pour réserver ce contenu aux utilisateurs Premium")

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
        return f"{self.user.username} a ajouté un(e) {self.content_type.model} (ID: {self.object_id}) à ses favoris"


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
        return f"{self.user.username} a téléchargé un(e) {self.content_type.model} (ID: {self.object_id})"



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

# ── NOTIFICATIONS ──
class Notification(models.Model):
    TYPES_NOTIF = [
        ('PRIERE', 'Prière'),
        ('WIRD', 'Wird'),
        ('ZIKR', 'Zikr'),
        ('NOUVEAU', 'Nouveau Contenu'),
        ('RAPPEL', 'Rappel Spirituel'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    titre = models.CharField(max_length=200)
    message = models.TextField()
    type_notif = models.CharField(max_length=20, choices=TYPES_NOTIF, default='RAPPEL')
    url_action = models.CharField(max_length=255, blank=True, null=True, help_text="URL vers laquelle rediriger au clic")
    est_lue = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"Notif ({self.type_notif}) pour {self.user.username}: {self.titre}"


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

# ── KAAMIL BI (Khatm du Coran) ──
class SessionKaamil(models.Model):
    titre = models.CharField(max_length=200, default="KAAMIL BI - Lecture du Coran", help_text="Titre de la session")
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions_kaamil_creees')
    est_prive = models.BooleanField(default=False, help_text="Si coché, accessible uniquement par lien")
    code_partage = models.CharField(max_length=50, blank=True, null=True, unique=True)
    date_debut = models.DateTimeField(auto_now_add=True)
    est_actif = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.est_prive and not self.code_partage:
            self.code_partage = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.titre} ({'Privé' if self.est_prive else 'Public'})"

class JukkiKaamil(models.Model):
    session = models.ForeignKey(SessionKaamil, on_delete=models.CASCADE, related_name='jukkis')
    numero = models.IntegerField(help_text="Numéro du Jukki (1 à 30)")
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='jukkis_pris')
    est_termine = models.BooleanField(default=False)
    date_prise = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('session', 'numero')
        ordering = ['numero']

    def __str__(self):
        return f"Jukki {self.numero} - {self.session.titre}"

@receiver(post_save, sender=SessionKaamil)
def creer_les_30_jukkis(sender, instance, created, **kwargs):
    if created:
        jukkis = [JukkiKaamil(session=instance, numero=i) for i in range(1, 31)]
        JukkiKaamil.objects.bulk_create(jukkis)


# ── QUIZZ ISLAMIQUE ──
class CategorieQuiz(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icone = models.CharField(max_length=50, default='fa-solid fa-book', help_text="Classe FontAwesome")

    def __str__(self):
        return self.nom

class NiveauQuiz(models.Model):
    numero = models.IntegerField(unique=True)
    nom = models.CharField(max_length=100)
    points_requis = models.IntegerField(default=0, help_text="Points cumulés nécessaires pour débloquer ce niveau")

    class Meta:
        ordering = ['numero']

    def __str__(self):
        return f"Niveau {self.numero}: {self.nom}"

class Question(models.Model):
    categorie = models.ForeignKey(CategorieQuiz, on_delete=models.CASCADE, related_name='questions')
    niveau = models.ForeignKey(NiveauQuiz, on_delete=models.CASCADE, related_name='questions')
    texte = models.TextField()
    points = models.IntegerField(default=10)
    explication = models.TextField(blank=True, null=True, help_text="Affiché après réponse pour éduquer le joueur")

    def __str__(self):
        return self.texte

class Choix(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choix')
    texte = models.CharField(max_length=255)
    est_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.texte} ({self.question.texte})"

class ScoreJoueur(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name='score_quiz')
    points_totaux = models.IntegerField(default=0)
    niveau_actuel = models.ForeignKey(NiveauQuiz, on_delete=models.SET_NULL, null=True, blank=True)

    def verifier_niveau(self):
        niveaux = NiveauQuiz.objects.filter(points_requis__lte=self.points_totaux).order_by('-points_requis')
        if niveaux.exists():
            self.niveau_actuel = niveaux.first()
            self.save()

    def __str__(self):
        return f"{self.utilisateur.username} - {self.points_totaux} pts"

@receiver(post_save, sender=User)
def creer_score_joueur(sender, instance, created, **kwargs):
    if created:
        ScoreJoueur.objects.create(utilisateur=instance)

class DefiMultijoueur(models.Model):
    createur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='defis_crees')
    code_partage = models.CharField(max_length=10, unique=True, blank=True)
    niveau_choisi = models.ForeignKey(NiveauQuiz, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    est_actif = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.code_partage:
            self.code_partage = str(uuid.uuid4())[:6].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Défi {self.code_partage} par {self.createur.username}"

class ParticipationDefi(models.Model):
    defi = models.ForeignKey(DefiMultijoueur, on_delete=models.CASCADE, related_name='participations')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date_participation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('defi', 'utilisateur')

    def __str__(self):
        return f"{self.utilisateur.username} - {self.score} pts sur Défi {self.defi.code_partage}"

# ── TAZAWWUDU-Ç-ÇIGHÂR (Gamification) ──

class TazawwudModule(models.Model):
    numero = models.IntegerField(unique=True)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    icone = models.CharField(max_length=100, default="fa-book-open")
    
    class Meta:
        ordering = ['numero']

    def __str__(self):
        return f"Module {self.numero} : {self.titre}"

class TazawwudLecon(models.Model):
    module = models.ForeignKey(TazawwudModule, on_delete=models.CASCADE, related_name="lecons")
    numero = models.IntegerField()
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    texte_source = models.TextField(help_text="Texte original du livre", blank=True, null=True)
    explication = models.TextField(help_text="Explication pédagogique", blank=True, null=True)
    a_retenir = models.TextField(help_text="Points clés (Markdown)", blank=True, null=True)
    vers_debut = models.IntegerField(blank=True, null=True)
    vers_fin = models.IntegerField(blank=True, null=True)
    est_revision_finale = models.BooleanField(default=False, help_text="Vrai si c'est la révision intense de fin de module")

    class Meta:
        ordering = ['module__numero', 'numero']

    def __str__(self):
        return f"{self.module.numero}.{self.numero} - {self.titre}"

class TazawwudQuestion(models.Model):
    TYPE_CHOICES = [
        ('qcm', 'QCM'),
        ('vrai_faux', 'Vrai/Faux'),
    ]
    lecon = models.ForeignKey(TazawwudLecon, on_delete=models.CASCADE, related_name="questions")
    texte = models.CharField(max_length=500)
    type_question = models.CharField(max_length=20, choices=TYPE_CHOICES, default='qcm')
    explication_reponse = models.TextField(help_text="S'affiche après la réponse pour expliquer")
    points = models.IntegerField(default=10)

    def __str__(self):
        return self.texte

class TazawwudChoix(models.Model):
    question = models.ForeignKey(TazawwudQuestion, on_delete=models.CASCADE, related_name="choix")
    texte = models.CharField(max_length=255)
    est_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.texte

class TazawwudConcept(models.Model):
    lecon = models.ForeignKey(TazawwudLecon, on_delete=models.CASCADE, related_name="concepts")
    titre = models.CharField(max_length=255)
    definition = models.TextField()

    def __str__(self):
        return self.titre

class TazawwudProgression(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="tazawwud_progression")
    module_courant = models.ForeignKey(TazawwudModule, on_delete=models.SET_NULL, null=True, blank=True)
    lecon_courante = models.ForeignKey(TazawwudLecon, on_delete=models.SET_NULL, null=True, blank=True)
    lecons_terminees = models.ManyToManyField(TazawwudLecon, related_name="users_termines", blank=True)
    concepts_maitrises = models.ManyToManyField(TazawwudConcept, related_name="users_maitrises", blank=True)
    concepts_a_revoir = models.ManyToManyField(TazawwudConcept, related_name="users_a_revoir", blank=True)
    score_total = models.IntegerField(default=0)
    serie_jours = models.IntegerField(default=0)
    derniere_activite = models.DateField(auto_now=True)

    def __str__(self):
        return f"Progression de {self.user.username}"

class TazawwudBadge(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    icone = models.CharField(max_length=100)
    condition = models.CharField(max_length=255, help_text="Description de la condition d'obtention")

    def __str__(self):
        return self.nom

class TazawwudUserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tazawwud_badges")
    badge = models.ForeignKey(TazawwudBadge, on_delete=models.CASCADE)
    date_obtention = models.DateTimeField(auto_now_add=True)
