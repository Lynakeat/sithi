from django.conf.urls.defaults import *
from django.views.generic.list import ListView

from models import FAQ

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=FAQ), name='faq'),
)