from django.conf.urls.defaults import *

urlpatterns = patterns('activebuys.apps.contacts.views',
    url(r'^$', 'contacts', name="contacts"),
)
