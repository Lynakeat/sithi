from django.conf import settings
from createsend import Subscriber, CreateSend


CreateSend.api_key = settings.CMONITOR_API_KEY


def _custom_fields(user):
    custom_fields = []
    cities = [i.cmonitor_name for i in user.subscribe_location.all()]
    if user.referred_email:
        custom_fields.append({'Key': 'ReferredBy', 'Value': user.referred_email})
    for city in cities:
        custom_fields.append({'Key': 'City', 'Value': city})
    return custom_fields
    

def subscribe(user):
    custom_fields = _custom_fields(user)
    subscriber = Subscriber()
    subscriber.add(settings.CMONITOR_LIST_ID,
                   user.email, user.get_full_name(), custom_fields, True)



def update(old_email, user):
    custom_fields = _custom_fields(user)
    subscriber = Subscriber(settings.CMONITOR_LIST_ID, old_email)
    subscriber.update(user.email, user.get_full_name(), custom_fields, True)
