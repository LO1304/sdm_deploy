import urllib.request
import sys
sys.stdout.reconfigure(encoding='utf-8')

filename = "Zadoul-moussafir.pdf"
filename_encoded = filename.replace(" ", "%20")

urls = [
    f"https://khassidaenpdf.net/BOOKS/{filename_encoded}",
    f"https://khassidaenpdf.net/BOOKS/{filename_encoded}.pdf"
]

for url in urls:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req)
        print(f"[+] Success: {url} (Status: {res.status})")
        print(f"   Content-Type: {res.headers.get('Content-Type')}")
        print(f"   Content-Length: {res.headers.get('Content-Length')}")
    except Exception as e:
        print(f"[-] Failed {url}: {e}")
