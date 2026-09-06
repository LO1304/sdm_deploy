import re
with open(r'C:\Users\ELECTRONIK SERVICES\.gemini\antigravity\brain\960644cd-f9f2-466a-aca1-eb96005018ef\.system_generated\steps\437\content.md', 'r', encoding='utf-8') as f:
    text = f.read()
print('Collections:', re.findall(r'collection\([\'"](.*?)[\'"]\)', text))
matches = re.findall(r'\{id:.*?,question:.*?,choix:\[.*?\]\}', text)
print('Found exact matches:', len(matches))
