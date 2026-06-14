from bibliotheque.models import Zikr, SessionZikrCommunautaire
from django.contrib.auth.models import User

def run():
    admin = User.objects.filter(is_superuser=True).first() or User.objects.first()

    # Mise a jour du texte arabe pour les Zikrs existants
    Zikr.objects.filter(titre__icontains='salaat').update(
        texte_arabe='صَلَّى اللّٰهُ عَلَى مُحَمَّد',
        transcription='Sallal Lahou Ala Mouhamad'
    )
    Zikr.objects.filter(titre__icontains='salatou').update(
        texte_arabe='صَلَّى اللّٰهُ عَلَى مُحَمَّد',
        transcription='Sallal Lahou Ala Mouhamad'
    )

    istighfar, _ = Zikr.objects.get_or_create(
        titre="Astaghfirullah", 
        defaults={
            'texte_arabe': 'أَسْتَغْفِرُ اللّٰهَ', 
            'transcription': 'Astaghfiroullah', 
            'traduction': 'Je demande pardon a Allah'
        }
    )
    # Forcer la mise a jour du texte arabe si deja existant
    istighfar.texte_arabe = 'أَسْتَغْفِرُ اللّٰهَ'
    istighfar.transcription = 'Astaghfiroullah'
    istighfar.save()
    
    salaat = Zikr.objects.filter(titre__icontains='salaat').first() or Zikr.objects.first()

    # 1. Istikhfar 1 million
    SessionZikrCommunautaire.objects.get_or_create(
        titre="Grand Istighfar",
        zikr=istighfar,
        defaults={'objectif_global': 1000000, 'createur': admin}
    )

    # 2. Salaat 1 million
    SessionZikrCommunautaire.objects.get_or_create(
        titre="Grande Salaat sur le Prophete",
        zikr=salaat,
        defaults={'objectif_global': 1000000, 'createur': admin}
    )

    # 3. Jeudi Nuit Salaat 12,000
    SessionZikrCommunautaire.objects.get_or_create(
        titre="Special Nuit du Jeudi (Vendredi)",
        zikr=salaat,
        defaults={'objectif_global': 12000, 'createur': admin}
    )
    print("Sessions et calligraphies arabes mises a jour avec succes !")

if __name__ == '__main__':
    run()
