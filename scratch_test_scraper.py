import urllib.request
import re

req = urllib.request.Request("https://khassidaenpdf.net/", headers={'User-Agent': 'Mozilla/5.0'})
res = urllib.request.urlopen(req)
html = res.read().decode('utf-8')

pattern1 = re.compile(r'\\"nomFrancais\\":\\"([^"\\]+)\\".*?\\"files\\":\[([^\]]+)\].*?\\"auteur\\":\\"([^"\\]+)\\"')
matches1 = pattern1.findall(html)

pattern2 = re.compile(r'\\"nomFrancais\\":\\"([^"\\]+)\\".*?\\"files\\":\[(.*?)\].*?\\"auteur\\":\\"([^"\\]+)\\"')
matches2 = pattern2.findall(html)

print(f"Matches with at least one file: {len(matches1)}")
print(f"Matches with any or no files: {len(matches2)}")

# Let's see the ones that have no files
for m in matches2:
    if m not in matches1:
        print(f"No files: {m[0]}")
