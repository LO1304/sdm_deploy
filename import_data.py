import os
import django
import requests
from django.core.files.base import ContentFile
from urllib.parse import unquote

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from bibliotheque.models import Khassida

def import_khassidas(limit=150):
    print("🚀 Début de l'importation MASSIVE...")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Liste étendue de Khassidas
    base_url = "https://khassidaenpdf.net/BOOKS/"
    filenames = [
        "Abuu Bakrin.pdf", "Afala tachkuruna.pdf", "Ahlu Badr.pdf", "Ahbabtou+fatahan.pdf", 
        "Ahonzu Billaahi.pdf", "Ajabani_Raboussama_1.pdf", "Al Baraka.pdf", "Al Muhaymin.pdf", 
        "Al Quraane.pdf", "Alaahu_kun_fayakun_Usni_Hala_1.pdf", "Assalamu_Alayka_1.pdf",
        "Asmaaul_Husna.pdf", "Baraka_1.pdf", "Dahabtou_1.pdf", "Fasubhaana_1.pdf", 
        "Ila_Siwa_1.pdf", "Jawartou_1.pdf", "Mafatihul_Bichri_1.pdf", "Matlabul_Fawzayni_1.pdf", 
        "Mawahibou_1.pdf", "Minanul_Baqi_1.pdf", "Mounadjat_1.pdf", "Nourou_Darayni_1.pdf", 
        "Sindidi_1.pdf", "Taysirul_Assir_1.pdf", "Wakana_haqqan_1.pdf", "Xarnu_bi.pdf",
        "Yaa_Khayra_Mawloudin.pdf", "Zayni.pdf", "Mubaraku.pdf", "Matalibul_Ihsan.pdf",
        "Jalibatul_Marakhib.pdf", "Hisnul_Abrar.pdf", "Fouzti.pdf", "Jaawartu.pdf"
    ]
    
    count = 0
    for filename in filenames:
        if count >= limit: break
        
        titre = unquote(filename).replace('.pdf', '').replace('.PDF', '').replace('_', ' ').replace('+', ' ')
        
        # Vérifier si déjà existant pour ne pas doublonner
        if Khassida.objects.filter(titre__iexact=titre.strip()).exists():
            print(f"⏭️ Sauter (déjà présent): {titre}")
            continue

        try:
            url = base_url + filename.replace(' ', '%20')
            print(f"📥 Téléchargement: {titre}...")
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200 and len(response.content) > 5000:
                khassida = Khassida(titre=titre.strip())
                khassida.fichier_pdf.save(filename, ContentFile(response.content), save=True)
                print(f"✅ Importé: {titre}")
                count += 1
        except Exception as e:
            print(f"⚠️ Erreur pour {titre}: {e}")

    print(f"\n🏁 Fin de l'importation. {count} nouveaux Khassidas ajoutés !")

if __name__ == "__main__":
    import_khassidas()
