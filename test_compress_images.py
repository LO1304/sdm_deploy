import io
import urllib.request
from pypdf import PdfReader, PdfWriter

url = "https://khassidaenpdf.net/BOOKS/Al%20Minahoul%20Miskiyyah.pdf"
print("Downloading...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    res = urllib.request.urlopen(req, timeout=30)
    pdf_bytes = res.read()
    print(f"Original size: {len(pdf_bytes) / 1024 / 1024:.2f} MB")
    
    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)
        
    writer.add_metadata({})
    
    # Compress content streams
    for page in writer.pages:
        page.compress_content_streams()
        try:
            for img in page.images:
                # Try to compress using img.replace
                img.replace(img.image, quality=30)
        except Exception as e:
            print(f"Image compression failed: {e}")
            
    writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)
    
    output = io.BytesIO()
    writer.write(output)
    compressed = output.getvalue()
    
    print(f"Compressed size: {len(compressed) / 1024 / 1024:.2f} MB")
except Exception as e:
    print(f"Error: {e}")
