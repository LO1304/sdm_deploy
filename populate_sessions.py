from bibliotheque.models import Zikr, SessionZikrCommunautaire
from django.contrib.auth.models import User

def merge_and_clean_duplicates():
    # Mapping from wrong (unaccented) titles to correct (accented) titles
    dups_map = {
        "Grande Salaat sur le Prophete": "Grande Salaat sur le Prophète",
        "Special Nuit du Jeudi (Vendredi)": "Spécial Nuit du Jeudi (Vendredi)",
    }
    
    for wrong_title, correct_title in dups_map.items():
        wrong_sessions = SessionZikrCommunautaire.objects.filter(titre=wrong_title)
        if wrong_sessions.exists():
            # Find or create correct session
            first_wrong = wrong_sessions.first()
            correct_session, created = SessionZikrCommunautaire.objects.get_or_create(
                titre=correct_title,
                defaults={
                    'zikr': first_wrong.zikr,
                    'objectif_global': first_wrong.objectif_global,
                    'createur': first_wrong.createur,
                    'est_actif': first_wrong.est_actif
                }
            )
            for ws in wrong_sessions:
                # Merge the counters
                correct_session.compteur_actuel += ws.compteur_actuel
                
                # Merge participations
                for part in ws.participations.all():
                    existing_part = correct_session.participations.filter(utilisateur=part.utilisateur).first()
                    if existing_part:
                        existing_part.contribution += part.contribution
                        existing_part.save()
                    else:
                        part.session = correct_session
                        part.save()
                
                # Delete the incorrect session
                ws.delete()
            
            correct_session.save()

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

    # Clean up and merge duplicates before creating new ones
    merge_and_clean_duplicates()

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
    print("Sessions et calligraphies arabes mises a jour avec succes !")

if __name__ == '__main__':
    run()
