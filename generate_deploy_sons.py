import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from bibliotheque.models import Son

def generate_script():
    sons = Son.objects.all()
    data = []
    for s in sons:
        data.append({
            "titre": s.titre,
            "auteur_voix": s.auteur_voix,
            "categorie": s.categorie,
            "fichier_audio": s.fichier_audio.name
        })
    
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
                'fichier_audio': item['fichier_audio']
            }}
        )
        if created:
            print(f"Ajouté : {{item['titre']}}")
        else:
            # Update to ensure file path is correct
            obj.fichier_audio = item['fichier_audio']
            obj.auteur_voix = item['auteur_voix']
            obj.save()
            print(f"Mis à jour : {{item['titre']}}")
    
    print("Tous les sons ont été synchronisés.")

if __name__ == '__main__':
    run()
"""
    with open("deploy_sons.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    print("deploy_sons.py généré avec succès!")

if __name__ == '__main__':
    generate_script()
