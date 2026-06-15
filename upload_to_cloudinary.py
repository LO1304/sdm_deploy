import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
import json

# Configuration de Cloudinary
cloudinary.config(
    cloud_name='dcajqzg2h',
    api_key='222919289611882',
    api_secret='oJ1C-UGV6emLDjKNr_vTom3ZsIM'
)

# Taille maximale de la version gratuite Cloudinary pour 'video' (100 Mo)
MAX_SIZE = 100 * 1024 * 1024

def run_upload():
    print("Démarrage du téléversement vers Cloudinary (Format Audio/Video < 100 Mo)...")
    
    successful_uploads = []

    # 1. Le fichier racine
    root_file = "media/audios/khassida/ACHINU_WKSM_KUREL_ASNAL_KHADIM_HT.mp3"
    if os.path.exists(root_file) and os.path.getsize(root_file) <= MAX_SIZE:
        url = upload_file(root_file, "media/audios/khassida/ACHINU_WKSM_KUREL_ASNAL_KHADIM_HT.mp3")
        if url:
            successful_uploads.append({
                "titre": "Achinu - Kurel Asnal Khadim HT",
                "auteur_voix": "Kurel Asnal Khadim HT",
                "categorie": "KHASSIDA",
                "lien_audio_externe": url
            })
    else:
        print(f"[SKIPPED] Fichier trop grand: {root_file.encode('ascii', 'replace').decode()}")

    # 2. Les fichiers Ramadan 2026
    ramadan_dir = os.path.join("media", "audios", "khassida", "Khassida Ramadan 2026")
    if os.path.exists(ramadan_dir):
        for filename in sorted(os.listdir(ramadan_dir)):
            if filename.endswith('.mp3') or filename.endswith('.m4a'):
                local_path = os.path.join(ramadan_dir, filename)
                public_id = f"media/audios/khassida/Khassida Ramadan 2026/{filename}"
                
                size = os.path.getsize(local_path)
                if size > MAX_SIZE:
                    print(f"[SKIPPED] {filename.encode('ascii', 'replace').decode()} ({size / 1024 / 1024:.1f} Mo)")
                    continue
                
                url = upload_file(local_path, public_id)
                if url:
                    # Extraire titre et auteur
                    titre = filename
                    for ext in ['.mp3', '.m4a']:
                        if titre.endswith(ext):
                            titre = titre[:-len(ext)]
                    titre_clean = titre.replace('_', ' ')
                    
                    auteur = ""
                    kourels = ["KUREL MACHRABUS CHAFI HT", "KUREL NURUD DARAYNI HT", "KUREL ASNA KHADIM HT", "KUREL ASNAL KHADIM HT", "KUREL MAFATIHUL BICHRI HT", "KUREL SERIGNE SALIOU MBACKE HT", "KUREL TAZAWUDUS SIKHAR HT", "KUREL WAKEUR SERIGNE MASSAMBA HT", "KUREL SERIGNE ABDUL AHAD MBACKE HT", "KOUREL 1 TOUTANK HTDKH", "Kourel 1 Kaolack HTDKH"]
                    for k in kourels:
                        if k.lower() in titre_clean.lower():
                            auteur = k.replace("KUREL", "Kurel").replace("KOUREL", "Kourel")
                            break
                    if not auteur:
                        artistes = ["Sgne Moustapha Diop", "Sgne Youssou Ndao", "Sgne Modou DIOP", "Sgne Moussa Gueye Ndar", "Sgne Abdoul Ahad Toure", "Serigne Abdou Rahmane", "Wa Keur Sgne Massamba", "Kourel Taverny"]
                        for a in artistes:
                            if a.lower() in titre_clean.lower():
                                auteur = a
                                break

                    successful_uploads.append({
                        "titre": titre_clean,
                        "auteur_voix": auteur,
                        "categorie": "KHASSIDA",
                        "lien_audio_externe": url
                    })

    # Generer le script deploy_sons.py mis a jour
    generate_deploy_script(successful_uploads)
    print("Téléversement terminé et deploy_sons.py mis à jour !")
    
    # Commit et push automatique
    print("Envoi vers GitHub...")
    os.system('git add deploy_sons.py bibliotheque/models.py bibliotheque/migrations/ bibliotheque/templates/')
    os.system('git commit -m "feat: Déploiement automatique des sons Cloudinary URL externe"')
    os.system('git push origin main')
    print("Déploiement déclenché sur Render !")

def upload_file(local_path, public_id):
    try:
        try:
            res = cloudinary.api.resource(public_id, resource_type='video')
            print(f"[Déjà présent] {public_id.encode('ascii', 'replace').decode()}")
            return res.get('secure_url')
        except cloudinary.exceptions.NotFound:
            pass
        
        print(f"[Upload] {public_id.encode('ascii', 'replace').decode()} ...")
        res = cloudinary.uploader.upload_large(
            local_path,
            resource_type='video',
            public_id=public_id,
            chunk_size=10000000
        )
        return res.get('secure_url')
    except Exception as e:
        print(f"[ERREUR] {public_id.encode('ascii', 'replace').decode()}: {str(e).encode('ascii', 'replace').decode()}")
        return None

def generate_deploy_script(data):
    script_content = f"""import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from bibliotheque.models import Son

SONS_DATA = {json.dumps(data, indent=4)}

def run():
    print("Insertion des sons dans la base de donnees de production...")
    for item in SONS_DATA:
        obj, created = Son.objects.get_or_create(
            titre=item['titre'],
            defaults={{
                'auteur_voix': item['auteur_voix'],
                'categorie': item['categorie'],
                'lien_audio_externe': item['lien_audio_externe']
            }}
        )
        if created:
            print(f"Ajouté : {{item['titre'].encode('ascii', 'replace').decode()}}")
        else:
            obj.lien_audio_externe = item['lien_audio_externe']
            obj.auteur_voix = item['auteur_voix']
            obj.save()
            print(f"Mis à jour : {{item['titre'].encode('ascii', 'replace').decode()}}")

if __name__ == '__main__':
    run()
"""
    with open("deploy_sons.py", "w", encoding="utf-8") as f:
        f.write(script_content)

if __name__ == '__main__':
    run_upload()
