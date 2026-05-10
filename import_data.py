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
    # On supprime les anciens imports qui sont corrompus
    print("🧹 Nettoyage des anciens fichiers corrompus...")
    Khassida.objects.all().delete()

    print(f"🚀 Début de l'importation PROPRE (Limite: {limit})...")
    
    # Headers pour se faire passer pour un navigateur réel
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://khassidaenpdf.net/'
    }

    urls = [
        "https://khassidaenpdf.net/BOOKS/Afala tachkuruna.pdf",
        "https://khassidaenpdf.net/BOOKS/Ahlu Badr.pdf",
        "https://khassidaenpdf.net/BOOKS/Ahbabtou+fatahan.pdf",
        "https://khassidaenpdf.net/BOOKS/Ahonzu Billaahi.pdf",
        "https://khassidaenpdf.net/BOOKS/Ajabani_Raboussama_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Al Baraka.pdf",
        "https://khassidaenpdf.net/BOOKS/Al Muhaymin.pdf",
        "https://khassidaenpdf.net/BOOKS/Al Quraane.pdf",
        "https://khassidaenpdf.net/BOOKS/Alaahu_kun_fayakun_Usni_Hala_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Assalamu_Alayka_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Baraka_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Dahabtou_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Fasubhaana_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Ila_Siwa_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Jawartou_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Mafatihul_Bichri_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Matlabul_Fawzayni_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Mawahibou_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Minanul_Baqi_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Mounadjat_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Nourou_Darayni_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Sindidi_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Taysirul_Assir_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Wakana_haqqan_1.pdf",
    ]
    
    count = 0
    for url in urls:
        if count >= limit: break
        
        titre = clean_title(url)
        
        try:
            print(f"📥 Téléchargement de '{titre}'...")
            # Encodage de l'URL pour gérer les espaces
            encoded_url = url.replace(' ', '%20')
            response = requests.get(encoded_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # Sécurité : un PDF valide fait généralement plus de 10 Ko
                if len(response.content) < 5000:
                    print(f"⚠️ Fichier trop petit ({len(response.content)} octets), probablement une page d'erreur.")
                    continue
                
                khassida = Khassida(titre=titre)
                khassida.fichier_pdf.save(f"{titre}.pdf", ContentFile(response.content), save=True)
                print(f"✅ Importé avec succès: {titre} ({len(response.content) // 1024} Ko)")
                count += 1
            else:
                print(f"❌ Erreur HTTP {response.status_code} pour {titre}")
        except Exception as e:
            print(f"⚠️ Erreur technique pour {titre}: {e}")

    print(f"\n🏁 Fin de l'importation. {count} Khassidas valides ajoutés !")

if __name__ == "__main__":
    import_khassidas()
