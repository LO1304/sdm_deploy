import urllib.request

urls_to_check = [
    "https://khassidaenpdf.net/sitemap.xml",
    "https://khassidaenpdf.net/robots.txt"
]

for url in urls_to_check:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req)
        content = res.read().decode('utf-8')
        print(f"--- {url} ---")
        print(content[:500])
        print("-" * 40)
    except Exception as e:
        print(f"Failed {url}: {e}")
