import os
import django
import io
import requests
import zipfile
import cloudinary.utils
from pypdf import PdfReader, PdfWriter

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
    
    print(f"Original size: {len(pdf_data) / 1024 / 1024:.2f} MB")
    
    reader = PdfReader(io.BytesIO(pdf_data))
    writer = PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)
        
    writer.add_metadata({})
    
    # Try replacing images
    images_count = 0
    for page in writer.pages:
        # Note: page.images might be list
        try:
            for img in page.images:
                # compress it!
                img.replace(img.image, quality=30)
                images_count += 1
        except Exception as e:
            print(f"Error compressing image: {e}")
            
    writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)
    
    output = io.BytesIO()
    writer.write(output)
    compressed = output.getvalue()
    
    print(f"Compressed size: {len(compressed) / 1024 / 1024:.2f} MB")
    print(f"Replaced {images_count} images.")
else:
    print("Failed to download zip")
