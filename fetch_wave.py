import urllib.request
import re
import json

def search():
    url = "https://en.wikipedia.org/wiki/Wave_Mobile_Money"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        print("Wikipedia length:", len(html))
        
        matches = re.findall(r'src="([^"]*Wave[^"]*(?:logo|png|svg)[^"]*)"', html, re.IGNORECASE)
        print("Matches:", matches)
        for m in matches:
            if m.startswith('//'):
                m = 'https:' + m
            if '/thumb/' in m:
                # remove thumb part to get original
                m = re.sub(r'/thumb(/.*)/[^/]+$', r'\1', m)
            print("Downloading:", m)
            
            try:
                img_data = urllib.request.urlopen(urllib.request.Request(m, headers={'User-Agent': 'Mozilla/5.0'})).read()
                with open('C:/Users/ELECTRONIK SERVICES/Desktop/SDM_Project/sdm_config/static/images/wave_logo.png', 'wb') as f:
                    f.write(img_data)
                print("Downloaded successfully!")
                return
            except Exception as e:
                print("Failed download:", e)
    except Exception as e:
        print("Wiki error:", e)

search()
