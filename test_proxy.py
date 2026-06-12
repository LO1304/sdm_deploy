import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from bibliotheque.models import Khassida
import cloudinary.utils
import zipfile
import io

k = Khassida.objects.get(id=10)
pdf_name = str(k.fichier_pdf)
print(f"pdf_name: {pdf_name}")

try:
    zip_url = cloudinary.utils.download_zip_url(
        public_ids=[pdf_name],
        resource_type='raw'
    )
    print(f"zip_url: {zip_url}")
    remote = requests.get(zip_url, timeout=30)
    print(f"zip_status: {remote.status_code}")
    if remote.status_code == 200:
        z = zipfile.ZipFile(io.BytesIO(remote.content))
        filename_in_zip = z.namelist()[0]
        print(f"File in zip: {filename_in_zip}")
    else:
        print(f"Error content: {remote.text}")
except Exception as e:
    print(f"Error: {e}")
