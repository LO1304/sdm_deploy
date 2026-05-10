import os
import django
import requests
from django.core.files.base import ContentFile
from urllib.parse import unquote
import cloudinary.uploader

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from bibliotheque.models import Khassida

def import_khassidas(limit=50):
    print("🧹 Nettoyage pour ré-importation propre...")
    Khassida.objects.all().delete()

    headers = {'User-Agent': 'Mozilla/5.0'}
    urls = [
        "https://khassidaenpdf.net/BOOKS/Afala tachkuruna.pdf",
        "https://khassidaenpdf.net/BOOKS/Ahlu Badr.pdf",
        "https://khassidaenpdf.net/BOOKS/Al Baraka.pdf",
        "https://khassidaenpdf.net/BOOKS/Mafatihul_Bichri_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Sindidi_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Taysirul_Assir_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Wakana_haqqan_1.pdf",
    ]
    
    count = 0
    for url in urls:
        if count >= limit: break
        try:
            filename = url.split('/')[-1]
            titre = unquote(filename).replace('.pdf', '').replace('_', ' ').replace('+', ' ')
            
            print(f"📥 Téléchargement: {titre}...")
            response = requests.get(url.replace(' ', '%20'), headers=headers, timeout=30)
            
            if response.status_code == 200:
                # Création de l'objet
                khassida = Khassida(titre=titre)
                
                # Sauvegarde du fichier avec extension explicite
                khassida.fichier_pdf.save(filename, ContentFile(response.content), save=True)
                
                print(f"✅ Importé: {khassida.fichier_pdf.url}")
                count += 1
        except Exception as e:
            print(f"⚠️ Erreur: {e}")

    print(f"\n🏁 Terminé: {count} Khassidas.")

if __name__ == "__main__":
    import_khassidas()
