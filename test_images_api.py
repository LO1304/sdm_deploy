import os
import django
import io
import requests
import zipfile
import cloudinary.utils
from pypdf import PdfReader

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

from bibliotheque.models import Khassida

k = Khassida.objects.get(id=10)
pdf_name = str(k.fichier_pdf)

# Configure cloudinary using settings
from django.conf import settings as conf_settings
import cloudinary
cloud_config = getattr(conf_settings, 'CLOUDINARY_STORAGE', {})
cloudinary.config(
    cloud_name=cloud_config.get('CLOUD_NAME', 'dcajqzg2h'),
    api_key=cloud_config.get('API_KEY', '222919289611882'),
    api_secret=cloud_config.get('API_SECRET', 'oJ1C-UGV6emLDjKNr_vTom3ZsIM'),
    secure=True,
)

zip_url = cloudinary.utils.download_zip_url(
    public_ids=[pdf_name],
    resource_type='raw'
)
remote = requests.get(zip_url, timeout=30)
if remote.status_code == 200:
    z = zipfile.ZipFile(io.BytesIO(remote.content))
    filename_in_zip = z.namelist()[0]
    pdf_data = z.read(filename_in_zip)
    
    reader = PdfReader(io.BytesIO(pdf_data))
    page = reader.pages[0]
    print("page.images type:", type(page.images))
    print("page.images dir:", dir(page.images))
    if page.images:
        print("First image:", page.images[0])
        print("First image type:", type(page.images[0]))
        print("First image dir:", dir(page.images[0]))
else:
    print("Failed to download zip")
