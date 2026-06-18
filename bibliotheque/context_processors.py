from .models import Notification
from django.db.utils import OperationalError, ProgrammingError

def notifications_processor(request):
    if request.user.is_authenticated:
        try:
            unread_count = Notification.objects.filter(user=request.user, est_lue=False).count()
            return {'unread_notifications_count': unread_count}
        except (OperationalError, ProgrammingError):
            # Évite de planter tout le site si les migrations ne sont pas encore passées sur le serveur
            return {'unread_notifications_count': 0}
    return {'unread_notifications_count': 0}
