import re

with open(r'C:\Users\ELECTRONIK SERVICES\.gemini\antigravity\brain\60f6ad2f-9483-414c-9bfc-9cae3e61e85a\.system_generated\steps\539\content.md', 'r', encoding='utf-8') as f:
    html = f.read()

# Look for URL bases
urls = re.findall(r'https?://[a-zA-Z0-9.-]+', html)
from collections import Counter
counts = Counter(urls)

for url, count in counts.most_common(20):
    print(f"{count}: {url}")
