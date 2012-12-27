from django.conf.urls.defaults import *
from django.views.generic.list import ListView
from django.views.generic.simple import redirect_to

from activebuys.apps.companies.models import Company, NonProfit
from activebuys.apps.companies.views import CategoryListView, LocationListView, LocationDetailView, LocationRedirectView

urlpatterns = patterns('',
    url(r'^partners/$', redirect_to, {'url': '/resources/'}),
    url(r'^partners/non-profits/$', redirect_to, {'url': 'non-profits/'}),
    url(r'^non-profits/$', ListView.as_view(model=NonProfit), name='non-profits'),
    # url(r'^resources/$', ListView.as_view(
    #     queryset=Company.objects.filter(is_partner=True),
    #     template_name='companies/partner_list.html')),
    url(r'^resources/$', 
        CategoryListView.as_view(), 
        name='resources'),
    url(r'^resources/(?P<slug>[-\w]+)/$', 
        LocationListView.as_view(), 
        name='resources-location-list'),   
    url(r'^resources/location/(?P<pk>\d+)/$', 
        LocationRedirectView.as_view()),
    url(r'^resources/location/(?P<slug>[-\w]+)/$', 
        LocationDetailView.as_view(), 
        name='resources-location-detail'),
)
