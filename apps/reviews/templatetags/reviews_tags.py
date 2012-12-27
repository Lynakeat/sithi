# django imports
from django import template
from django.contrib.contenttypes.models import ContentType

# review imports
from activebuys.apps.reviews.models import Review, Vote
from activebuys.apps.reviews import utils as reviews_utils

from django.contrib.auth.models import User, AnonymousUser

register = template.Library()

@register.inclusion_tag('reviews/reviews_for_instance.html', takes_context=True)
def reviews_for_instance(context, instance):
    """
    """
    request = context.get("request")
    ctype = ContentType.objects.get_for_model(instance)    
    has_rated = reviews_utils.has_rated(request, instance)
    reviews = reviews_utils.get_reviews_for_instance(instance)

    return {
        "reviews" : reviews,
        "has_rated" : has_rated,
        "content_id" : instance.id,
        "content_type_id" : ctype.id,
        "MEDIA_URL" : context.get("MEDIA_URL")
    }

@register.inclusion_tag('reviews/average_for_instance.html', takes_context=True)
def average_for_instance(context, instance):
    """
    """
    average, amount = reviews_utils.get_average_for_instance(instance)
    return {
        "average" : average,
        "amount": amount,
    }

@register.simple_tag
def is_voting(request, obj, vote_type):
    """
    Returns `True` in case `user` is following `obj`, else `False`
    """
    result = ""
    if isinstance(request.user, AnonymousUser):
        result = 0 < Vote.objects.filter(review=obj,ip_address=reviews_utils.get_client_ip(request), vote_type=vote_type, active=True).count()
    else:
        result = 0 < Vote.objects.filter(review=obj,user=request.user, vote_type=vote_type, active=True).count()

    if result:
        return "voted"
    else:
        return ""

