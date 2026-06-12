import urllib.request
import re

book_id = "cm7hpi84w00kstmb5oih2peb5"
print(f"Testing with book ID: {book_id}")

book_urls = [
    f"https://khassidaenpdf.net/khassida/{book_id}",
    f"https://khassidaenpdf.net/book/{book_id}",
    f"https://khassidaenpdf.net/document/{book_id}",
    f"https://khassidaenpdf.net/pdf/{book_id}"
]

for book_url in book_urls:
    try:
        req = urllib.request.Request(book_url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req)
        book_html = res.read().decode('utf-8')
        print(f"Success for {book_url}")
        
        # look for pdf links in this page
        pdf_links = re.findall(r'href=[\'"]([^\'"]+\.pdf)[\'"]', book_html)
        print("PDF links found:", pdf_links)
        
        # look for any hrefs containing khassidaenpdf
        hrefs = re.findall(r'href=[\'"]([^\'"]+)[\'"]', book_html)
        print("First 10 hrefs:", hrefs[:10])
        
        break
    except urllib.error.HTTPError as e:
        print(f"Failed to fetch {book_url}: {e.code}")
    except Exception as e:
        print(f"Failed to fetch {book_url}: {e}")
