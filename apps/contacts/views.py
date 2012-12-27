from django.http import Http404
from activebuys.apps.utils.views import render_to, render_json

from activebuys.apps.contacts.models import Message
from activebuys.apps.contacts.forms import MessageForm

def contacts(request):
    if request.GET.get('ajax'):
        return contacts_post(request)
    return contacts_get(request)


@render_to('contacts/message_form.html')
def contacts_get(request):
    form = MessageForm()
    return {'form': form}

@render_json
def contacts_post(request):
    success = False
    if request.method=="POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages = ''
            success = True
        else:
            messages = form.errors
    else:
        raise Http404
    return {'success': success, 'messages': messages}
