import urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')

# Test different URL patterns for PDFs
filename = "Abuu Bakrin.pdf"
filename_encoded = filename.replace(" ", "%20")

patterns = [
    f"https://khassidaenpdf.net/files/{filename_encoded}",
    f"https://khassidaenpdf.net/pdf/{filename_encoded}",
    f"https://khassidaenpdf.net/api/files/{filename_encoded}",
    f"https://khassidaenpdf.net/api/download/{filename_encoded}",
    f"https://khassidaenpdf.net/uploads/{filename_encoded}",
    f"https://khassidaenpdf.net/public/{filename_encoded}",
    f"https://khassidaenpdf.net/khassidas/{filename_encoded}",
    f"https://khassidaenpdf.net/documents/{filename_encoded}",
]

for url in patterns:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response = urllib.request.urlopen(req, timeout=10)
        print(f"✅ {response.status} - {url}")
        print(f"   Content-Type: {response.headers.get('Content-Type')}")
        print(f"   Content-Length: {response.headers.get('Content-Length')}")
        break
    except urllib.error.HTTPError as e:
        print(f"❌ {e.code} - {url}")
    except Exception as e:
        print(f"❌ Error - {url}: {e}")
