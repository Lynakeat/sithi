from django.conf.urls.defaults import *

urlpatterns = patterns('activebuys.apps.deals.views',
    url(r'^$', 'detail', name="deals-home"),
    url(r'^([-\w]+)/$', 'detail', name='deals-detail'),
    url(r'^([-\w]+)/buy/$', 'buy', name='deals-buy'),
    url(r'^ajax/pastdeals/$', 'ajax_past_deals', name='ajax-past-deals'),
)
