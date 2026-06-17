import urllib.request
import urllib.parse
import re

url = "https://www.wave.com/en/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    matches = re.findall(r'href="([^"]*logo[^"]*\.png|[^"]*logo[^"]*\.svg|[^"]*wave[^"]*\.png|[^"]*wave[^"]*\.svg)"', html, re.IGNORECASE)
    matches += re.findall(r'src="([^"]*logo[^"]*\.png|[^"]*logo[^"]*\.svg|[^"]*wave[^"]*\.png|[^"]*wave[^"]*\.svg)"', html, re.IGNORECASE)
    for m in set(matches):
        print(m)
        if not m.startswith('http'):
            m = urllib.parse.urljoin(url, m)
        try:
            img = urllib.request.urlopen(urllib.request.Request(m, headers={'User-Agent': 'Mozilla/5.0'})).read()
            with open('C:/Users/ELECTRONIK SERVICES/Desktop/SDM_Project/sdm_config/static/images/wave_logo.png', 'wb') as f:
                f.write(img)
            print("Successfully downloaded", m)
            break
        except Exception as e:
            print("Error downloading", m, e)
except Exception as e:
    print('Error:', e)
