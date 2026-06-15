import os, sys, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'sdm_config.settings'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()
from bibliotheque.models import ContenuDuJour

# Delete the fake entries (ID 3-6) that were auto-generated
deleted = ContenuDuJour.objects.filter(id__gte=3).delete()
print(f"Deleted: {deleted}")

# Verify what remains
remaining = ContenuDuJour.objects.all()
print(f"Remaining entries: {remaining.count()}")
last = ContenuDuJour.objects.last()
if last:
    print(f"Now showing on home: ID={last.id} date={last.date}")
