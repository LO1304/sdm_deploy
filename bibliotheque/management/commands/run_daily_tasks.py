import os
import random
from datetime import datetime, timezone
from django.core.management.base import BaseCommand
from bibliotheque.models import SessionZikrCommunautaire, Zikr, ContenuDuJour, Profile
from django.contrib.auth.models import User
import firebase_admin
from firebase_admin import credentials, messaging

MASALIKOUL_DJINANE_VERSES = [
    ("Le repentir est une obligation immédiate pour tout pécheur.", "التوبة واجبة على الفور لكل عاصٍ"),
    ("Purifie ton cœur de l'ostentation, de la jalousie, de la haine et de l'orgueil.", "طهر قلبك من الرياء والكبر"),
    ("La meilleure des provisions est la crainte pieuse (Taqwa).", "وخير الزاد التقوى"),
    ("Consacre ton temps à l'évocation d'Allah (Zikr).", "واصرف أوقاتك في ذكر الله"),
    ("L'amour du Prophète (PSL) est la clé de la réussite.", "ومحبة النبي مفتاح الفلاح"),
    ("Garde le silence sauf pour dire du bien.", "واحفظ لسانك إلا من خير"),
    ("Pardonne à ceux qui t'ont fait du tort.", "واعف عمن ظلمك"),
    ("La patience dans les épreuves est une lumière.", "والصبر في البلاء ضياء"),
    ("Ne méprise aucun musulman, car le secret d'Allah peut être en lui.", "ولا تحتقرن مسلماً فإن سر الله قد يكون فيه"),
    ("Sois constant dans tes prières à l'heure.", "وداوم على الصلاة في وقتها"),
    ("La pire désobéissance est celle qui endurcit le cœur et fait oublier Dieu.", ""),
    ("La science sans la pratique n'est qu'un fardeau inutile pour l'âme.", ""),
    ("Mets ta confiance absolue en Allah, Il te suffira comme protecteur.", ""),
    ("La gratitude envers les bienfaits de ton Seigneur en assure l'augmentation.", ""),
    ("Recherche la compagnie des vertueux pour élever ton état spirituel.", ""),
    ("Dompte tes passions et ton ego, car ils sont tes plus grands ennemis.", ""),
    ("Le repentir sincère efface le passé et illumine l'avenir du croyant.", ""),
    ("Évite la médisance et la calomnie, elles consument les bonnes actions.", ""),
    ("Fais preuve d'humilité, car quiconque s'humilie pour Allah sera élevé.", ""),
    ("Sois bienveillant envers les faibles et les nécessiteux.", ""),
    ("Le contentement est un trésor inépuisable pour le cœur pur.", ""),
    ("N'attends rien des créatures, place toute ton espérance en le Créateur.", ""),
    ("La prière nocturne est une douceur que seuls les sincères goûtent.", ""),
    ("Parle avec douceur et courtoisie à tous les êtres humains.", ""),
    ("Évite la colère, car elle obscurcit le discernement et la foi.", ""),
    ("Sois honnête dans tes transactions et fidèle à tes engagements.", ""),
    ("Médite chaque jour sur la création d'Allah pour renforcer ta certitude.", ""),
    ("Le souvenir de la mort purifie le cœur de l'attachement mondain.", ""),
    ("Sois utile aux autres, car le meilleur des hommes est le plus utile.", ""),
    ("Ne retarde jamais une bonne action, car le lendemain ne t'appartient pas.", "")
]

class Command(BaseCommand):
    help = "Tâche quotidienne : Contenu du jour, Zikr du jeudi, Notifications"

    def handle(self, *args, **options):
        self.stdout.write("--- Début des tâches quotidiennes ---")
        
        # 1. GÉNÉRER LE CONTENU DU JOUR (Masalikoul Djinane - Un verset différent chaque jour)
        today = datetime.now(timezone.utc)
        day_of_year = today.timetuple().tm_yday
        verse_index = (day_of_year - 1) % len(MASALIKOUL_DJINANE_VERSES)
        verse = MASALIKOUL_DJINANE_VERSES[verse_index]
        fr_text, ar_text = verse
        ContenuDuJour.objects.create(
            verset_du_jour=f"{fr_text}",
            beuyit_du_jour="Tiré de Masalikoul Djinane",
            rappel_dujour="Méditez sur ces paroles de Cheikh Ahmadou Bamba aujourd'hui."
        )
        self.stdout.write(f"Contenu du jour généré pour le jour {day_of_year} de l'année (verset {verse_index + 1}).")

        # 2. VÉRIFIER SI C'EST JEUDI
        today = datetime.now(timezone.utc)
        if today.weekday() == 3:  # 0=Lundi, 3=Jeudi
            self.stdout.write("C'est Jeudi ! Renouvellement du Zikr...")
            admin = User.objects.filter(is_superuser=True).first() or User.objects.first()
            salaat = Zikr.objects.filter(titre__icontains='salaat').first()
            
            if salaat and admin:
                # Désactiver les anciennes sessions "Nuit du Jeudi"
                SessionZikrCommunautaire.objects.filter(titre__icontains="Nuit du Jeudi", est_actif=True).update(est_actif=False)
                
                # Créer la nouvelle session
                nouvelle_session = SessionZikrCommunautaire.objects.create(
                    titre=f"Spécial Nuit du Jeudi ({today.strftime('%d/%m')})",
                    zikr=salaat,
                    objectif_global=12000,
                    createur=admin
                )
                self.stdout.write(f"Nouvelle session créée : {nouvelle_session.titre}")
                
                # 3. ENVOYER LA NOTIFICATION PUSH FCM
                self.send_push_notification(
                    title="Nuit du Vendredi",
                    body="La session de 12 000 Salaat a commencé ! Rejoignez la communauté."
                )
        else:
            self.stdout.write("Aujourd'hui n'est pas jeudi, pas de session spéciale.")
            
        self.stdout.write("--- Fin des tâches ---")

    def send_push_notification(self, title, body):
        # Initialiser Firebase si ce n'est pas déjà fait
        try:
            if not firebase_admin._apps:
                firebase_admin.initialize_app()
        except Exception as e:
            self.stdout.write(f"Impossible d'initialiser Firebase Admin: {e}")
            return

        tokens = list(Profile.objects.exclude(fcm_token__isnull=True).exclude(fcm_token="").values_list('fcm_token', flat=True))
        
        if not tokens:
            self.stdout.write("Aucun token FCM trouvé pour envoyer des notifications.")
            return

        try:
            # FCM limite à 500 tokens par requête, on prend les 500 premiers (à optimiser avec un batching pour bcp d'utilisateurs)
            message = messaging.MulticastMessage(
                notification=messaging.Notification(title=title, body=body),
                tokens=tokens[:500] 
            )
            response = messaging.send_multicast(message)
            self.stdout.write(f"Notification envoyée. Succès: {response.success_count}, Échecs: {response.failure_count}")
        except Exception as e:
            self.stdout.write(f"Erreur FCM: {str(e)}")
