from datetime import datetime,  timedelta
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from activebuys.apps.accounts.models import AccountDeal

TIMELIMIT = getattr(settings, 'NEW_DEAL_TIME_LIFE', 30)

class Command(BaseCommand):
    help = 'Remove deals that user not finished'

    def handle(self, *args, **options):
        now = datetime.now()
        accountdeal_list = AccountDeal.objects.filter(status=AccountDeal.NEW).\
            filter(timestamp__lte=now-timedelta(minutes=TIMELIMIT))
        for i in accountdeal_list:
            i.delete()
