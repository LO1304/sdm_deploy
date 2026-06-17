from django.core.management.base import BaseCommand
from bibliotheque.models import Khassida
from django.core.files.base import ContentFile
import fitz
import cloudinary.utils
import urllib.request
import zipfile
import io

class Command(BaseCommand):
    help = 'Génère les images de couverture à partir de la première page des PDF'

    def handle(self, *args, **options):
        qs = Khassida.objects.filter(image_couverture='').exclude(fichier_pdf='')
        self.stdout.write(f'Trouve {qs.count()} Khassidas a traiter.')

        for k in qs:
            try:
                pdf_name = str(k.fichier_pdf)
                zip_url = cloudinary.utils.download_zip_url(public_ids=[pdf_name], resource_type='raw')
                
                req = urllib.request.Request(zip_url, headers={'User-Agent': 'Mozilla/5.0'})
                res = urllib.request.urlopen(req)
                zip_bytes = res.read()
                
                with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
                    pdf_bytes = None
                    for info in z.infolist():
                        if info.filename.lower().endswith('.pdf'):
                            pdf_bytes = z.read(info)
                            break
                            
                if pdf_bytes:
                    doc = fitz.open(stream=pdf_bytes, filetype='pdf')
                    if len(doc) > 0:
                        page = doc.load_page(0)
                        pix = page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0))
                        img_bytes = pix.tobytes('jpeg')
                        
                        filename = f'cover_{k.id}.jpg'
                        k.image_couverture.save(filename, ContentFile(img_bytes), save=True)
                        self.stdout.write(self.style.SUCCESS(f'-> Couverture generee pour {k.titre}'))
            except Exception as e:
                self.stderr.write(f'-> Erreur pour {k.titre}: {e}')
