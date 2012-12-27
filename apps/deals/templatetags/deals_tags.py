import datetime
from django import template
from django.db import models

register = template.Library()
Deal = models.get_model('deals','Deal')

@register.inclusion_tag('deals/_past_deals.html')
def past_deals(count=3):
    deals = Deal.objects.filter(past_featured=True,
                                end_time__lte=datetime.datetime.now())[:count]
    return {'deals':deals}

@register.inclusion_tag('deals/_more_deals.html')
def more_deals(exclude=None, count=4):
    """ show all active deals exclude current deal """
    deals = Deal.active.all().order_by('?')
    if exclude:
        deals = deals.exclude(id=exclude.id)
    return {'deals':deals[:count]}

@register.inclusion_tag('deals/_active_deals.html')
def active_deals(exclude=None, count=4):
    """ show all active deals """
    deals = Deal.active.all().order_by('?')
    return {'deals':deals}   

@register.filter
def is_limit_reached(deal, user):
    return deal.per_user and\
            (deal.per_user + deal.gift_limit) <=\
            user.accountdeal_set.filter(deal=deal).count()

