from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from activebuys.apps.zipcodes.views import SaveZipCodeToSessionView
from uturn.decorators import uturn

urlpatterns = patterns('',
    url(r'^$', uturn(SaveZipCodeToSessionView.as_view()), name='zipcode_update'),
    url(r'^success/$', TemplateView.as_view(template_name='zipcodes/success.html'), name='zipcode_success'),
)