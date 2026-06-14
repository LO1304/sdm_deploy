"""
Script pour :
1. Supprimer les anciens Sons qui ne marchent pas
2. Importer tous les fichiers audio du dossier Khassida Ramadan 2026
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from bibliotheque.models import Son

def run():
    # 1. SUPPRIMER tous les anciens sons
    old_count = Son.objects.count()
    Son.objects.all().delete()
    print(f"Supprime {old_count} ancien(s) son(s).")

    # 2. IMPORTER le fichier à la racine de khassida
    root_file = "audios/khassida/ACHINU_WKSM_KUREL_ASNAL_KHADIM_HT.mp3"
    Son.objects.create(
        titre="Achinu - Kurel Asnal Khadim HT",
        auteur_voix="Kurel Asnal Khadim HT",
        categorie="KHASSIDA",
        fichier_audio=root_file
    )
    print("Ajoute: Achinu - Kurel Asnal Khadim HT")

    # 3. IMPORTER tous les fichiers du dossier Khassida Ramadan 2026
    ramadan_dir = os.path.join("media", "audios", "khassida", "Khassida Ramadan 2026")
    
    if not os.path.exists(ramadan_dir):
        print(f"ERREUR: Le dossier {ramadan_dir} n'existe pas!")
        return
    
    count = 0
    for filename in sorted(os.listdir(ramadan_dir)):
        if not (filename.endswith('.mp3') or filename.endswith('.m4a')):
            continue
        
        # Construire le chemin relatif pour Django FileField
        relative_path = f"audios/khassida/Khassida Ramadan 2026/{filename}"
        
        # Nettoyer le titre à partir du nom du fichier
        titre = filename
        # Enlever l'extension
        for ext in ['.mp3', '.m4a']:
            if titre.endswith(ext):
                titre = titre[:-len(ext)]
                break
        
        # Extraire l'auteur/kourel si possible
        auteur = ""
        titre_clean = titre.replace('_', ' ')
        
        # Patterns courants pour les kourels
        kourels = [
            "KUREL MACHRABUS CHAFI HT",
            "KUREL NURUD DARAYNI HT",
            "KUREL ASNA KHADIM HT", 
            "KUREL ASNAL KHADIM HT",
            "KUREL MAFATIHUL BICHRI HT",
            "KUREL SERIGNE SALIOU MBACKE HT",
            "KUREL TAZAWUDUS SIKHAR HT",
            "KUREL WAKEUR SERIGNE MASSAMBA HT",
            "KUREL SERIGNE ABDUL AHAD MBACKE HT",
            "KOUREL 1 TOUTANK HTDKH",
        ]
        for k in kourels:
            if k.lower() in titre_clean.lower():
                auteur = k.replace("KUREL", "Kurel").replace("KOUREL", "Kourel")
                break
        
        # Si pas de kourel trouvé, chercher les noms d'artistes
        if not auteur:
            artistes = [
                "Sgne Moustapha Diop",
                "Sgne Youssou Ndao",
                "Sgne Modou DIOP",
                "Sgne Moussa Gueye Ndar",
                "Sgne Abdoul Ahad Toure",
                "Serigne Abdou Rahmane",
                "Wa Keur Sgne Massamba",
                "Kourel Taverny",
                "Kurel 1 Kaolack HTDKH",
            ]
            for a in artistes:
                if a.lower() in titre_clean.lower():
                    auteur = a
                    break
        
        # Vérifier si le fichier n'est pas un doublon (fichiers avec (1), (2))
        if '(1)' in titre or '(2)' in titre:
            print(f"  Ignore (doublon): {filename.encode('ascii', 'replace').decode()}")
            continue
        
        Son.objects.create(
            titre=titre_clean,
            auteur_voix=auteur,
            categorie="KHASSIDA",
            fichier_audio=relative_path
        )
        count += 1
        print(f"  Ajoute: {titre_clean.encode('ascii', 'replace').decode()[:60]}...")

    print(f"\nTotal: {count} sons importes depuis Khassida Ramadan 2026")
    print(f"Total dans la base: {Son.objects.count()} sons")

if __name__ == '__main__':
    run()
