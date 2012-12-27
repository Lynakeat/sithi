# django imports
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.db.models import Avg

# review imports
from activebuys.apps.reviews.models import Review

# def get_best_rated():
#     """Returns the best rated instance for all models.
#     """
#     cursor = connection.cursor()
#     cursor.execute("""SELECT avg(score), content_type_id, content_id
#                       FROM reviews_review
#                       WHERE active=%s
#                       GROUP BY content_id
#                       ORDER BY score DESC""", [True])

#     try:
#         score, content_type_id, content_id = cursor.fetchone()
#         ctype = ContentType.objects.get_for_id(content_type_id)
#         content = ctype.model_class().objects.get(pk=content_id)
#         return content, score
#     except (TypeError, ObjectDoesNotExist):
#         return None

def get_reviews_for_instance(instance):
    """Returns active reviews for given instance.
    """
    return Review.objects.active().filter(location=instance)

def get_average_for_instance(instance):
    """Returns the average score and the amount of reviews for the given
    instance. Takes only active reviews into account.

    Returns {'score__avg': <average>}
    """
    return Review.objects.active().filter(location=instance).aggregate(Avg('score'))


def has_rated(request, instance):
    """Returns True if the current user has already rated for the given
    instance.
    """

    try:
        if request.user.is_authenticated():
            review = Review.objects.get(location=instance, user=request.user)
        else:
            review = Review.objects.get(location=instance)
    except ObjectDoesNotExist:
        return False
    else:
        return True

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
