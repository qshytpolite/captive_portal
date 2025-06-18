from django.core.management.base import BaseCommand
from portal.models import CaptiveSession
from django.utils import timezone


class Command(BaseCommand):
    help = 'Auto-deactivate expired or old captive sessions'

    def handle(self, *args, **options):
        now = timezone.now()
        expired = CaptiveSession.objects.filter(
            voucher__expires_at__lt=now,
            is_active=True
        )
        count = expired.update(is_active=False)
        self.stdout.write(f"Deactivated {count} expired sessions.")
