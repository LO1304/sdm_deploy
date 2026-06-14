from bibliotheque.models import Zikr, SessionZikrCommunautaire
from django.contrib.auth.models import User

def run():
    admin = User.objects.filter(is_superuser=True).first() or User.objects.first()

    istighfar, _ = Zikr.objects.get_or_create(
        titre="Astaghfirullah", 
        defaults={
            'texte_arabe': 'أَسْتَغْفِرُ اللّٰهَ', 
            'transcription': 'Astaghfirullah', 
            'traduction': 'Je demande pardon à Allah'
        }
    )
    
    salaat = Zikr.objects.filter(titre__icontains='salaat').first() or Zikr.objects.first()

    # 1. Istikhfar 1 million
    SessionZikrCommunautaire.objects.get_or_create(
        titre="Grand Istighfar",
        zikr=istighfar,
        defaults={'objectif_global': 1000000, 'createur': admin}
    )

    # 2. Salaat 1 million
    SessionZikrCommunautaire.objects.get_or_create(
        titre="Grande Salaat sur le Prophète",
        zikr=salaat,
        defaults={'objectif_global': 1000000, 'createur': admin}
    )

    # 3. Jeudi Nuit Salaat 12,000
    SessionZikrCommunautaire.objects.get_or_create(
        titre="Spécial Nuit du Jeudi (Vendredi)",
        zikr=salaat,
        defaults={'objectif_global': 12000, 'createur': admin}
    )
    print("Les 3 sessions communautaires ont été créées avec succès !")

if __name__ == '__main__':
    run()
