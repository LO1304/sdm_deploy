import os
import sys
import tempfile
import asyncio
import django
from django.core.files import File

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from bibliotheque.models import Son
from telethon import TelegramClient

# Remplissez vos identifiants ici (obtenus sur my.telegram.org)
API_ID = input("Entrez votre API_ID Telegram : ")
API_HASH = input("Entrez votre API_HASH Telegram : ")
PHONE_NUMBER = input("Entrez votre numéro de téléphone (ex: +221770000000) : ")

# Nom de la chaîne
CHANNEL_USERNAME = 'koureloukhaidayi'

async def main():
    print(f"Connexion à Telegram...")
    client = TelegramClient('sdm_session', API_ID, API_HASH)
    
    # Demande le code SMS si c'est la première connexion
    await client.start(phone=PHONE_NUMBER)
    print("Connexion réussie !")
    
    print(f"Analyse de la chaîne @{CHANNEL_USERNAME}...")
    
    # Récupérer les messages (on limite à 100 pour commencer, vous pouvez changer la limite)
    messages = await client.get_messages(CHANNEL_USERNAME, limit=100)
    
    audio_count = 0
    for message in messages:
        if message.audio or message.voice or message.document:
            # Vérifier si c'est bien un fichier audio
            is_audio = False
            if message.audio or message.voice:
                is_audio = True
            elif message.document and message.document.mime_type.startswith('audio/'):
                is_audio = True
                
            if is_audio:
                audio_count += 1
                titre = message.message or f"Audio Telegram {message.id}"
                # Nettoyer un peu le titre s'il est long
                titre = titre.split('\n')[0][:200]
                
                # Vérifier si on l'a déjà
                if Son.objects.filter(titre__iexact=titre, categorie='KHASSIDA').exists():
                    print(f"Ignoré (déjà existant) : {titre}")
                    continue
                
                print(f"Téléchargement de : {titre}...")
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tmp_path = tmp.name
                    
                try:
                    await client.download_media(message, tmp_path)
                    
                    # Sauvegarder dans Django (ça l'envoie sur Cloudinary)
                    son = Son(titre=titre, auteur_voix="Kourelou Khaidayi", categorie='KHASSIDA', est_premium=False)
                    with open(tmp_path, 'rb') as f:
                        # Le nom du fichier sera basé sur l'ID Telegram
                        filename = f"telegram_{message.id}.mp3"
                        son.fichier_audio.save(filename, File(f), save=True)
                    
                    print(f" => Enregistré avec succès : {titre}")
                except Exception as e:
                    print(f"Erreur pour {titre} : {e}")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

    print(f"Terminé ! {audio_count} audios trouvés et traités.")

if __name__ == '__main__':
    # Lance le script asynchrone
    asyncio.run(main())
