from django import template
from activebuys.apps.companies.models import NonProfit

register = template.Library()

@register.inclusion_tag('companies/_featured_nonprofit.html')
def featured_nonprofit(deal):
    featured = deal.nonprofit
    if not featured:
        try:
            featured = NonProfit.objects.filter(featured=True)[0]
        except IndexError:
            pass
    return {'company': featured}
