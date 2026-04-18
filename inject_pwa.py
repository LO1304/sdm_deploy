import os
import glob

template_dir = r"c:\Users\ELECTRONIK SERVICES\Desktop\SDM_Project\sdm_config\bibliotheque\templates\bibliotheque"

head_injection = """
    <!-- PWA -->
    <link rel="manifest" href="/static/manifest.json">
    <meta name="theme-color" content="#040B08">
    <link rel="apple-touch-icon" href="/static/images/icons/icon-192x192.png">
"""

sw_script = """
<!-- Service Worker Registration -->
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
      navigator.serviceWorker.register('/sw.js').then(function(registration) {
        console.log('ServiceWorker registration successful');
      }, function(err) {
        console.log('ServiceWorker registration failed: ', err);
      });
    });
  }
</script>
"""

# Include index and all others
for file_path in glob.glob(os.path.join(template_dir, "*.html")):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Skip if already injected
        if "manifest.json" in content or "serviceWorker.register" in content:
            continue
            
        modified = False

        if "<head>" in content or "<head " in content:
            # Replace first instance of <head>
            content = content.replace("<head>", "<head>" + head_injection, 1)
            modified = True
            
        # We also need to inject at the end of body
        if "</body>" in content:
            content = content.replace("</body>", sw_script + "</body>", 1)
            modified = True
            
        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Injected PWA into {os.path.basename(file_path)}")
    except Exception as e:
        print(f"Failed on {file_path}: {e}")

print("Done")
