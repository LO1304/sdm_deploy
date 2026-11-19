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

                    # 1. Upload Cloudinary (video/upload) avec fallback local automatique
                    secure_url = ''
                    try:
                        import cloudinary.uploader
                        up = cloudinary.uploader.upload(
                            tmp_path,
                            resource_type='video',
                            folder='media/audios/telegram/khassida',
                            public_id=f"tg_{CHANNEL_USERNAME}_{message.id}",
                        )
                        secure_url = up.get('secure_url') or ''
                    except Exception as ce:
                        print(f"  [Cloudinary fallback local] {ce}")

                    if not secure_url:
                        import shutil
                        from django.conf import settings
                        local_dir = os.path.join(settings.BASE_DIR, 'static', 'audios_locaux', 'khassida')
                        os.makedirs(local_dir, exist_ok=True)
                        local_fname = f"tg_{CHANNEL_USERNAME}_{message.id}.mp3"
                        shutil.copy2(tmp_path, os.path.join(local_dir, local_fname))
                        secure_url = f"/static/audios_locaux/khassida/{local_fname}"

                    Son.objects.create(
                        titre=titre,
                        auteur_voix=f"Kourel @{CHANNEL_USERNAME}",
                        categorie='KHASSIDA',
                        lien_audio_externe=secure_url,
                        est_premium=False,
                    )
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
