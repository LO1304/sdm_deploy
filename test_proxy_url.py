import urllib.request
try:
    req = urllib.request.Request('http://127.0.0.1:8000/proxy-pdf/khassida/10/')
    res = urllib.request.urlopen(req)
    print(res.status)
except Exception as e:
    print(f"Error: {e}")
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8')[:1000])
