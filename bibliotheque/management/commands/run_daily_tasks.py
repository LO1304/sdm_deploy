import os
import random
from datetime import datetime, timezone
from django.core.management.base import BaseCommand
from bibliotheque.models import SessionZikrCommunautaire, Zikr, ContenuDuJour, Profile
from django.contrib.auth.models import User
import firebase_admin
from firebase_admin import credentials, messaging

MASALIKOUL_DJINANE_VERSES = [
    "Le repentir est une obligation immédiate pour tout pécheur.",
    "Purifie ton cœur de l'ostentation et de l'orgueil.",
    "La meilleure des provisions est la crainte pieuse (Taqwa).",
    "Consacre ton temps à l'évocation d'Allah (Zikr).",
    "L'amour du Prophète (PSL) est la clé de la réussite.",
    "Garde le silence sauf pour dire du bien.",
    "Pardonne à ceux qui t'ont fait du tort.",
    "La patience dans les épreuves est une lumière.",
    "Ne méprise aucun musulman, car le secret d'Allah peut être en lui.",
    "Sois constant dans tes prières à l'heure."
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
        ContenuDuJour.objects.create(
            verset_du_jour=f"{verse}",
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
                
                # 3. ENVOYER LA NOTIFICATION
                self.send_notifications(
                    title="Nuit du Vendredi",
                    body="La session de 12 000 Salaat a commencé ! Rejoignez la communauté.",
                    notif_type='ZIKR',
                    url='/communaute/zikr/'
                )
        else:
            self.stdout.write("Aujourd'hui n'est pas jeudi, pas de session spéciale.")
            
        # 3. RAPPEL QUOTIDIEN WIRD
        self.send_notifications(
            title="Votre Wird Quotidien",
            body=f"C'est un nouveau jour ! {verse}",
            notif_type='WIRD',
            url='/collection/wird/'
        )
            
        self.stdout.write("--- Fin des tâches ---")

    def send_notifications(self, title, body, notif_type='RAPPEL', url='/'):
        from bibliotheque.models import Notification
        
        # Filtre sur les préférences
        pref_field = 'notif_nouveau_contenu'
        if notif_type == 'WIRD' or notif_type == 'ZIKR':
            pref_field = 'notif_wird'
        elif notif_type == 'PRIERE':
            pref_field = 'notif_prieres'
            
        # Création interne en base de données
        users = User.objects.filter(**{f"profile__{pref_field}": True})
        notifs = [Notification(user=u, titre=title, message=body, type_notif=notif_type, url_action=url) for u in users]
        if notifs:
            Notification.objects.bulk_create(notifs)

        # Envoi Push (FCM)
        try:
            if not firebase_admin._apps:
                firebase_admin.initialize_app()
        except Exception as e:
            self.stdout.write(f"Impossible d'initialiser Firebase Admin: {e}")
            return

        tokens = list(Profile.objects.filter(user__in=users).exclude(fcm_token__isnull=True).exclude(fcm_token="").values_list('fcm_token', flat=True))
        
        if not tokens:
            self.stdout.write("Aucun token FCM valide trouvé.")
            return

        try:
            message = messaging.MulticastMessage(
                notification=messaging.Notification(title=title, body=body),
                data={'url': url},
                tokens=tokens[:500] 
            )
            response = messaging.send_multicast(message)
            self.stdout.write(f"Push FCM envoyés. Succès: {response.success_count}, Échecs: {response.failure_count}")
        except Exception as e:
            self.stdout.write(f"Erreur FCM: {str(e)}")
