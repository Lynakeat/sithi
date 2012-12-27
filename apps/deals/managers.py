from datetime import datetime
from django.db import models


class ActiveDealManager(models.Manager):
    def get_query_set(self):
        """ Returns only "active" Deals:
         - which are current according to date range
         - and marked as `featured`
        """
        qs = super(ActiveDealManager, self).get_query_set()
        return qs.filter(end_time__gte=datetime.now(), start_time__lte=datetime.now(), featured=True)


class AllowedDealManager(models.Manager):
    def get_query_set(self):
        """ Returns only allowed to buy Deals
            All not expired deals and deal that was started
            and they could be open after expiration
        """
        Q = models.Q
        now = datetime.now()
        qs = super(AllowedDealManager, self).get_query_set()
        return qs.filter(Q(start_time__lte=now, end_time__gte=now) | \
                         Q(start_time__lte=now, open_after_expire=True))
