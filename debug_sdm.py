import os
import sys
import django
from pathlib import Path

# Ajouter le dossier courant au path pour trouver sdm_config
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from django.conf import settings
from django.contrib.staticfiles import finders

print("\n" + "="*40)
print("   DIAGNOSTIC STATIQUE - SDM MOURIDE")
print("="*40)

print(f"\n📂 BASE_DIR : {settings.BASE_DIR}")
print(f"📦 STATIC_ROOT : {settings.STATIC_ROOT}")
print(f"🔗 STATICFILES_DIRS : {settings.STATICFILES_DIRS}")
print(f"☁️  DEFAULT_FILE_STORAGE : {settings.DEFAULT_FILE_STORAGE}")

print("\n🔍 RECHERCHE DES FICHIERS CLES :")
for file_name in ['manifest.json', 'css/base.css', 'admin/js/theme.js']:
    found = finders.find(file_name)
    if found:
        print(f"  ✅ [TROUVÉ] {file_name}")
        print(f"     -> {found}")
    else:
        print(f"  ❌ [NON TROUVÉ] {file_name}")

print("\n📁 VERIFICATION PHYSIQUE DES DOSSIERS :")
paths_to_check = {
    "Static racine": os.path.join(settings.BASE_DIR, 'static'),
    "Static App": os.path.join(settings.BASE_DIR, 'bibliotheque', 'static'),
    "Static Build (Dest)": settings.STATIC_ROOT
}

for name, path in paths_to_check.items():
    if os.path.exists(path):
        files = os.listdir(path)
        print(f"  ✅ {name} ({path}) : EXISTE ({len(files)} fichiers/dossiers)")
        if len(files) < 5:
            print(f"     Contenu : {files}")
    else:
        print(f"  ❌ {name} ({path}) : N'EXISTE PAS")

print("\n" + "="*40 + "\n")
