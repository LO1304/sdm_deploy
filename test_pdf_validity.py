import os
import django
import requests
import cloudinary.utils
import zipfile
import io
from pypdf import PdfReader

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from bibliotheque.models import Khassida

k = Khassida.objects.get(id=10)
pdf_name = str(k.fichier_pdf)

zip_url = cloudinary.utils.download_zip_url(
    public_ids=[pdf_name],
    resource_type='raw'
)
remote = requests.get(zip_url, timeout=30)
if remote.status_code == 200:
    z = zipfile.ZipFile(io.BytesIO(remote.content))
    filename_in_zip = z.namelist()[0]
    pdf_data = z.read(filename_in_zip)
    
    try:
        reader = PdfReader(io.BytesIO(pdf_data))
        print(f"PDF is valid. Number of pages: {len(reader.pages)}")
    except Exception as e:
        print(f"PDF is corrupted! Error: {e}")
else:
    print(f"Failed to download zip: {remote.status_code}")
