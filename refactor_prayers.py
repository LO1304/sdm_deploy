import re
import os

index_path = 'bibliotheque/templates/bibliotheque/index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Extract script from index.html
script_match = re.search(r'{% block extra_js %}\s*<script>(.*?)</script>\s*{% endblock %}', index_content, re.DOTALL)
if script_match:
    prayer_script = script_match.group(1)
    
    # Remove the script from index.html
    index_content = index_content[:script_match.start()] + index_content[script_match.end():]
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    # Make prayer script null-safe
    prayer_script = prayer_script.replace('const ap = document.getElementById(\'adhan-player\');', "const ap = document.getElementById('adhan-player') || new Audio('/static/audio/adhan.mp3');")
    prayer_script = prayer_script.replace('toggleBtn.className', 'if(toggleBtn) toggleBtn.className')
    prayer_script = prayer_script.replace('toggleIcon.className', 'if(toggleIcon) toggleIcon.className')
    prayer_script = prayer_script.replace("document.getElementById('clock').textContent", "if(document.getElementById('clock')) document.getElementById('clock').textContent")
    prayer_script = prayer_script.replace("document.getElementById('next-name').textContent", "if(document.getElementById('next-name')) document.getElementById('next-name').textContent")
    prayer_script = prayer_script.replace("document.getElementById('countdown').textContent", "if(document.getElementById('countdown')) document.getElementById('countdown').textContent")
    prayer_script = prayer_script.replace("document.getElementById('countdown-sec').textContent", "if(document.getElementById('countdown-sec')) document.getElementById('countdown-sec').textContent")
    prayer_script = prayer_script.replace("document.getElementById('loc-city').textContent", "if(document.getElementById('loc-city')) document.getElementById('loc-city').textContent")
    
    # Fix the UI slots update
    prayer_script = prayer_script.replace(
        "document.querySelector('.ph-slot[data-prayer=\"Fajr\"] .slot-time').textContent = PT.Fajr;",
        "if(document.querySelector('.ph-slot[data-prayer=\"Fajr\"]')) document.querySelector('.ph-slot[data-prayer=\"Fajr\"] .slot-time').textContent = PT.Fajr;"
    )
    prayer_script = prayer_script.replace(
        "document.querySelector('.ph-slot[data-prayer=\"Dhuhr\"] .slot-time').textContent = PT.Dhuhr;",
        "if(document.querySelector('.ph-slot[data-prayer=\"Dhuhr\"]')) document.querySelector('.ph-slot[data-prayer=\"Dhuhr\"] .slot-time').textContent = PT.Dhuhr;"
    )
    prayer_script = prayer_script.replace(
        "document.querySelector('.ph-slot[data-prayer=\"Asr\"] .slot-time').textContent = PT.Asr;",
        "if(document.querySelector('.ph-slot[data-prayer=\"Asr\"]')) document.querySelector('.ph-slot[data-prayer=\"Asr\"] .slot-time').textContent = PT.Asr;"
    )
    prayer_script = prayer_script.replace(
        "document.querySelector('.ph-slot[data-prayer=\"Maghrib\"] .slot-time').textContent = PT.Maghrib;",
        "if(document.querySelector('.ph-slot[data-prayer=\"Maghrib\"]')) document.querySelector('.ph-slot[data-prayer=\"Maghrib\"] .slot-time').textContent = PT.Maghrib;"
    )
    prayer_script = prayer_script.replace(
        "document.querySelector('.ph-slot[data-prayer=\"Isha\"] .slot-time').textContent = PT.Isha;",
        "if(document.querySelector('.ph-slot[data-prayer=\"Isha\"]')) document.querySelector('.ph-slot[data-prayer=\"Isha\"] .slot-time').textContent = PT.Isha;"
    )
    
    # Fix compass
    prayer_script = prayer_script.replace(
        "const compass = document.getElementById('compass');",
        "const compass = document.getElementById('compass');\n        if(!compass) return;"
    )

    # Append to sdm_main.js
    main_js_path = 'static/js/sdm_main.js'
    with open(main_js_path, 'a', encoding='utf-8') as f:
        f.write("\n\n/* ═══ GLOBAL PRAYER SYSTEM ═══ */\n")
        f.write(prayer_script)

print("Extracted and injected global prayer script safely.")
