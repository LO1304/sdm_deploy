import os
import django
import requests
from django.core.files.base import ContentFile
from urllib.parse import unquote

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from bibliotheque.models import Khassida

def clean_title(url):
    filename = url.split('/')[-1]
    title = filename.replace('.pdf', '').replace('.PDF', '')
    title = unquote(title).replace('_', ' ').replace('+', ' ')
    return title.strip()

def import_khassidas(limit=50):
    print("🧹 Nettoyage final des fichiers mal indexés...")
    Khassida.objects.all().delete()

    print(f"🚀 Importation avec forçage du type de fichier...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

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
        titre = clean_title(url)
        try:
            print(f"📥 Récupération de '{titre}'...")
            encoded_url = url.replace(' ', '%20')
            response = requests.get(encoded_url, headers=headers, timeout=30)
            
            if response.status_code == 200 and len(response.content) > 10000:
                khassida = Khassida(titre=titre)
                
                # ON FORCE LE NOM AVEC EXTENSION PDF
                file_name = f"{titre.replace(' ', '_')}.pdf"
                
                # Sauvegarde directe
                khassida.fichier_pdf.save(file_name, ContentFile(response.content), save=True)
                
                # PETIT HACK : On s'assure que l'URL est propre
                print(f"✅ OK: {titre} -> URL: {khassida.fichier_pdf.url}")
                count += 1
        except Exception as e:
            print(f"⚠️ Erreur: {e}")

    print(f"\n🏁 Importation terminée : {count} fichiers prêts.")

if __name__ == "__main__":
    import_khassidas()
