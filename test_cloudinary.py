import os, sys, io, zipfile
sys.path.insert(0, '.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'sdm_config.settings'
import django; django.setup()
from bibliotheque.models import Khassida
import cloudinary, cloudinary.utils
from django.conf import settings
import requests

cc = settings.CLOUDINARY_STORAGE
cloudinary.config(
    cloud_name=cc['CLOUD_NAME'], 
    api_key=cc['API_KEY'], 
    api_secret=cc['API_SECRET'], 
    secure=True
)

k = Khassida.objects.first()
pdf_name = str(k.fichier_pdf)

print(f"Trying ZIP workaround for {pdf_name}")
zip_url = cloudinary.utils.download_zip_url(
    public_ids=[pdf_name],
    resource_type='raw'
)

print(f"ZIP URL: {zip_url[:100]}...")
r = requests.get(zip_url)
print(f"HTTP {r.status_code}")

if r.status_code == 200:
    try:
        # Load ZIP in memory
        z = zipfile.ZipFile(io.BytesIO(r.content))
        print("Files in ZIP:", z.namelist())
        
        # Extract the first file
        filename = z.namelist()[0]
        pdf_data = z.read(filename)
        print(f"Extracted PDF size: {len(pdf_data)} bytes")
        print(f"Starts with: {pdf_data[:10]}")
    except Exception as e:
        print("Error processing ZIP:", e)
