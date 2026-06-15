import re

file_path = 'bibliotheque/templates/bibliotheque/zikr_compteur.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_content = '{% extends "bibliotheque/layout.html" %}\n\n'

# Extract CSS
style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
if style_match:
    new_content += '{% block extra_head %}\n<style>\n' + style_match.group(1).strip() + '\n</style>\n{% endblock %}\n\n'

# Extract body
body_match = re.search(r'(<audio id="aud".*?</div><!-- /screen -->)', content, re.DOTALL)
html_part = body_match.group(1) if body_match else ''

overlay_match = re.search(r'(<!-- ADD SALAT SHEET -->.*?</div>\n</div>)', content, re.DOTALL)
if overlay_match:
    html_part += '\n\n' + overlay_match.group(1)

modal_match = re.search(r'(<!-- ══════════════════════════\s+CONGRATS MODAL\s+══════════════════════════ -->.*?</div>\n\n</div>)', content, re.DOTALL)
if modal_match:
    html_part += '\n\n' + modal_match.group(1)

new_content += '{% block content %}\n' + html_part + '\n{% endblock %}\n\n'

# Extract script
script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if script_match:
    script_content = script_match.group(1)
    
    script_content = re.sub(
        r'const DEFAULT_SALATS = \[.*?\];',
        '''const DEFAULT_SALATS = [
  {
    id: 's0',
    nom:   '{{ zikr.titre|escapejs }}',
    arabe: '{{ zikr.texte_arabe|escapejs }}',
    trans: '{{ zikr.texte_a_repeter|default:zikr.transcription|escapejs }}',
    goal:  {{ zikr.objectif_par_defaut|default:33 }},
    count: 0
  },
  { id:'s1', nom:'Istighfar',  arabe:'أَسْتَغْفِرُ اللَّهَ', trans:'Astaghfirullah', goal:100, count:0 },
  { id:'s2', nom:'Salat Nabi', arabe:'صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ', trans:'Sallallahu Alaihi Wasallam', goal:100, count:0 },
];''',
        script_content,
        flags=re.DOTALL
    )

    new_content += '{% block extra_js %}\n<script>\n' + script_content.strip() + '\n</script>\n{% endblock %}\n'

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Zikr refactored!')
