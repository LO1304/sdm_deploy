import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from bibliotheque.models import Khassida

k = Khassida.objects.get(id=10)
print(f"Titre: {k.titre}")
print(f"Fichier PDF name: {k.fichier_pdf.name if k.fichier_pdf else 'AUCUN'}")
if k.fichier_pdf:
    print(f"Fichier PDF url: {k.fichier_pdf.url}")
