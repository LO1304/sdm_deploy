import os
import requests
import tempfile
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from django.core.management.base import BaseCommand
from django.core.files import File
from bibliotheque.models import Son

class Command(BaseCommand):
    help = 'Télécharge les audios Xam Xam depuis Podcloud et les sauvegarde dans la base (upload sur Cloudinary)'

    def handle(self, *args, **kwargs):
        rss_url = 'https://khassida.lepodcast.fr/rss'
        self.stdout.write(self.style.SUCCESS(f"Téléchargement du flux RSS: {rss_url}"))
        
        try:
            resp = requests.get(rss_url, timeout=15)
            resp.raise_for_status()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur RSS: {e}"))
            return

        root = ET.fromstring(resp.content)
        channel = root.find('channel')
        ns = {'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}

        items = channel.findall('item')
        self.stdout.write(self.style.SUCCESS(f"Trouvé {len(items)} épisodes dans le RSS"))

        for item in items:
            title_el = item.find('title')
            if title_el is None or not title_el.text: continue
            title = title_el.text.strip()
            
            enclosure = item.find('enclosure')
            if enclosure is None: continue
            audio_url = enclosure.get('url', '')
            if not audio_url: continue
            
            author_el = item.find(f'{{{ns["itunes"]}}}author')
            if author_el is None:
                creator_el = item.find('{http://purl.org/dc/elements/1.1/}creator')
                author = creator_el.text.strip() if creator_el is not None and creator_el.text else 'Serigne Abdou Rahmane Mbacke'
            else:
                author = author_el.text.strip() if author_el.text else 'Serigne Abdou Rahmane Mbacke'
            
            # Vérifier si ce titre existe déjà avec un fichier
            son = Son.objects.filter(titre__iexact=title, categorie='XAM_XAM').first()
            if son and son.fichier_audio:
                self.stdout.write(f"Ignoré (déjà téléchargé): {title}")
                continue
                
            if not son:
                son = Son(titre=title, auteur_voix=author, categorie='XAM_XAM', est_premium=False)

            self.stdout.write(f"Téléchargement de l'audio: {title} ...")
            try:
                r = requests.get(audio_url, stream=True, timeout=30)
                r.raise_for_status()
                
                parsed = urlparse(audio_url)
                filename = os.path.basename(parsed.path)
                if not filename.endswith('.mp3'):
                    filename = f"xamxam_{son.id or 'new'}.mp3"
                    
                with tempfile.NamedTemporaryFile(delete=True) as tmp:
                    for chunk in r.iter_content(chunk_size=8192):
                        tmp.write(chunk)
                    tmp.flush()
                    
                    with open(tmp.name, 'rb') as f:
                        son.fichier_audio.save(filename, File(f), save=True)
                        son.lien_audio_externe = ''
                        son.save()
                        
                self.stdout.write(self.style.SUCCESS(f" => Sauvegardé avec succès: {filename}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erreur téléchargement {title}: {e}"))

        self.stdout.write(self.style.SUCCESS("Terminé! Les audios ont été téléchargés et sauvegardés."))
