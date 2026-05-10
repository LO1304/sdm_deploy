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
    # Extrait le nom du fichier de l'URL
    filename = url.split('/')[-1]
    # Enlève l'extension .pdf
    title = filename.replace('.pdf', '').replace('.PDF', '')
    # Remplace les underscores et + par des espaces
    title = unquote(title).replace('_', ' ').replace('+', ' ')
    return title.strip()

def import_khassidas(limit=50):
    print(f"🚀 Début de l'importation (Limite: {limit})...")
    
    # Liste simplifiée extraite du sitemap pour le test
    urls = [
        "https://khassidaenpdf.net/BOOKS/Afala tachkuruna.pdf",
        "https://khassidaenpdf.net/BOOKS/Ahlu Badr.pdf",
        "https://khassidaenpdf.net/BOOKS/Ahyaytu mawlidinabi.pdf",
        "https://khassidaenpdf.net/BOOKS/Al Baraka.pdf",
        "https://khassidaenpdf.net/BOOKS/Al Muhaymin.pdf",
        "https://khassidaenpdf.net/BOOKS/Al Mujibu.pdf",
        "https://khassidaenpdf.net/BOOKS/Al Qaribu.pdf",
        "https://khassidaenpdf.net/BOOKS/Alam nashra.pdf",
        "https://khassidaenpdf.net/BOOKS/Albaaqii.pdf",
        "https://khassidaenpdf.net/BOOKS/Asmau_Ahlul_Badr_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Assalamu_Alayka_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Baraka_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Dahabtou_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Fasubhaana_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Ila_Siwa_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Jawartou_1.pdf",
        "https://khassidaenpdf.net/BOOKS/Khassaid_1.pdf",
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
        
        # Vérifie si déjà existant
        if Khassida.objects.filter(titre=titre).exists():
            print(f"⏩ Saut de '{titre}' (déjà présent)")
            continue
            
        try:
            print(f"📥 Téléchargement de '{titre}'...")
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                khassida = Khassida(titre=titre)
                # On sauvegarde le fichier dans le champ FileField (Cloudinary s'occupe du reste)
                khassida.fichier_pdf.save(f"{titre}.pdf", ContentFile(response.content), save=True)
                print(f"✅ Importé: {titre}")
                count += 1
            else:
                print(f"❌ Erreur HTTP {response.status_code} pour {titre}")
        except Exception as e:
            print(f"⚠️ Erreur pour {titre}: {e}")

    print(f"\n🏁 Fin de l'importation. {count} nouveaux Khassidas ajoutés !")

if __name__ == "__main__":
    import_khassidas()
