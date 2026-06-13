import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdm_config.settings')
django.setup()

with open('data_dump.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', exclude=['auth.permission', 'contenttypes', 'admin.logentry', 'sessions.session', 'bibliotheque.historiqueconsultation'], stdout=f)
