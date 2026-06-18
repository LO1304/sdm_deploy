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
            cmd.send_notifications(
                title=f"Nouveau {model_name} disponible !",
                body=f"Découvrez '{instance.titre}' dès maintenant.",
                notif_type='NOUVEAU',
                url='/dashboard/'
            )
        except Exception:
            pass
