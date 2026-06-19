import os
import random
from datetime import datetime, timezone, timedelta
from django.core.management.base import BaseCommand
from bibliotheque.models import Profile, Notification
from django.contrib.auth.models import User
import firebase_admin
from firebase_admin import credentials, messaging
from adhan import adhan
from adhan.methods import MUSLIM_WORLD_LEAGUE

class Command(BaseCommand):
    help = "Tâche exécutée chaque minute pour l'Adhan et les rappels de Wird"

    def handle(self, *args, **options):
        now_utc = datetime.now(timezone.utc)
        self.stdout.write(f"--- Vérification des prières à {now_utc.strftime('%H:%M:%S')} UTC ---")
        
        # Initialisation Firebase si besoin
        if not firebase_admin._apps:
            try:
                firebase_admin.initialize_app()
            except Exception as e:
                self.stdout.write(f"Impossible d'initialiser Firebase Admin: {e}")
                return

        # Récupérer tous les utilisateurs ayant activé les notifs de prière et ayant des coordonnées
        profiles = Profile.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
        
        for profile in profiles:
            if not profile.fcm_token:
                continue

            try:
                params = MUSLIM_WORLD_LEAGUE # Muslim World League (ou un autre au choix)
                
                # Le calcul se fait pour la date actuelle en UTC mais selon les coordonnées
                date_tuple = (now_utc.year, now_utc.month, now_utc.day)
                prayer_times = adhan(
                    day=date_tuple,
                    timezone_offset=0, # On calcule en UTC car now_utc est en UTC
                    longitude=profile.longitude,
                    latitude=profile.latitude,
                    parameters=params
                )

                # Format de prayer_times : (fajr, shuruq, dhuhr, asr, maghrib, isha) en heures décimales UTC
                names = ["Fadjr", "Chourouq", "Dhuhr", "Asr", "Maghrib", "Isha"]
                
                for i, pt_dec in enumerate(prayer_times):
                    if i == 1: continue # On saute shuruq
                    name = names[i]
                    
                    h = int(pt_dec)
                    m = int(round((pt_dec - h) * 60))
                    
                    if m == 60:
                        h += 1
                        m = 0
                    h = h % 24

                    if now_utc.hour == h and now_utc.minute == m:
                        if profile.notif_prieres:
                            self.send_push(profile.fcm_token, f"L'heure du {name}", f"Il est l'heure de la prière de {name}. Allah Akbar!", "/collection/coran/")
                    
                    # RAPPEL WIRD 5 MIN APRÈS FADJR ET ASR
                    if name in ["Fadjr", "Asr"] and profile.notif_wird:
                        wird_m = m + 5
                        wird_h = h
                        if wird_m >= 60:
                            wird_h += 1
                            wird_m -= 60
                        wird_h = wird_h % 24
                        
                        if now_utc.hour == wird_h and now_utc.minute == wird_m:
                            self.send_push(profile.fcm_token, "Wird Mahouz", f"C'est le moment de réciter votre Wird Mahouz ({name}).", "/collection/wird/")
                            
            except Exception as e:
                self.stdout.write(f"Erreur pour l'utilisateur {profile.user.id} : {e}")

    def send_push(self, token, title, body, url):
        try:
            message = messaging.Message(
                notification=messaging.Notification(title=title, body=body),
                data={'url': url},
                token=token
            )
            response = messaging.send(message)
            self.stdout.write(f"Push FCM envoyé à {token[:10]}... pour {title}")
        except Exception as e:
            self.stdout.write(f"Erreur d'envoi FCM : {str(e)}")
