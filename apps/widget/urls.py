from django.conf.urls.defaults import *

urlpatterns = patterns('activebuys.apps.widget.views',
    url(r'^widget/$', 'widget', name='widget'),
)
