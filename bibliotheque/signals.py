from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Khassida, Coran, Son, Zikr, Wird
from bibliotheque.management.commands.run_daily_tasks import Command as DailyTasksCommand

@receiver(post_save, sender=Khassida)
@receiver(post_save, sender=Coran)
@receiver(post_save, sender=Son)
@receiver(post_save, sender=Zikr)
@receiver(post_save, sender=Wird)
def notify_new_content(sender, instance, created, **kwargs):
    if created:
        try:
            cmd = DailyTasksCommand()
            model_name = sender.__name__
            if sender is Khassida:
                title = f"📚 Nouveau Khassida : {instance.titre}"
                body = f"Le Khassida « {instance.titre} » vient d'être ajouté à la bibliothèque SDM. Ouvrez-le pour lire ou le garder hors-ligne."
                url = f"/lire/khassida/{instance.id}/"
            elif sender is Coran:
                title = f"📖 Nouveau Coran / Jukki : {instance.titre}"
                body = f"« {instance.titre} » est disponible dans l'espace Saint Coran."
                url = f"/lire/coran/{instance.id}/"
            elif sender is Son:
                title = f"🎧 Nouvel Audio : {instance.titre}"
                body = f"Écoutez « {instance.titre} » ({getattr(instance, 'auteur_voix', '') or 'Kourel Mouride'}) dans l'Audiothèque."
                url = f"/collection/son/?autoplay={instance.id}"
            else:
                title = f"Nouveau {model_name} : {instance.titre}"
                body = f"Découvrez « {instance.titre} » dès maintenant sur SDM Mouride."
                url = "/"
            cmd.send_notifications(
                title=title[:190],
                body=body[:300],
                notif_type='NOUVEAU',
                url=url
            )
        except Exception:
            pass
