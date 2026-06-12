import urllib.request
import re
import json

req = urllib.request.Request("https://khassidaenpdf.net/", headers={'User-Agent': 'Mozilla/5.0'})
res = urllib.request.urlopen(req)
html = res.read().decode('utf-8')

# The books are in a JSON array. 
# We can find the start of the array: "books":[...
# or we can find all {"id":"..."} objects using regex and parse them as JSON.

# Let's clean the html from backslashes to make it pure JSON.
clean_html = html.replace('\\"', '"').replace('\\\\', '\\')

# Find all JSON objects that have an "id" and "nomFrancais"
pattern = re.compile(r'\{"id":"[a-z0-9]+","nomFrancais":"[^"]+".*?\}')
matches = pattern.findall(clean_html)

print(f"Total potential book objects: {len(matches)}")

parsed_books = []
for m in matches:
    try:
        # Some objects might be cut off by the regex, let's just count how many we can parse
        # Since it's a greedy/lazy match, we might have issues if there are nested objects.
        # But looking at the structure: "files":["a","b"] -> no nested objects except arrays.
        obj = json.loads(m)
        if "nomFrancais" in obj:
            parsed_books.append(obj)
    except Exception as e:
        pass

print(f"Successfully parsed books: {len(parsed_books)}")
