from django.conf.urls.defaults import *
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView

from activebuys.apps.business.models import Feature
from activebuys.apps.business.forms import FeatureForm

urlpatterns = patterns('',
    url(r'^business/success/$', TemplateView.as_view(
            template_name="business/business_form.html"
        ),
        name="business-success"
    ),
    url(r'^business/$', CreateView.as_view(
            form_class=FeatureForm,
            model=Feature,
            template_name="business/business_form.html",
            success_url='/business/success/'  # don't understand reverse('business-success')
        ),
        name="business"
    ),

    # Employer
    url(r'^employer/success/$', TemplateView.as_view(
            template_name="business/employer_form.html"
        ),
        name="employer-success"
    ),
    url(r'^employer/$', CreateView.as_view(
            form_class=FeatureForm,
            model=Feature,
            template_name="business/employer_form.html",
            success_url='/employer/success/'  # don't understand reverse('business-success')
        ),
        name="employer"
    ),

    # Affiliate
    url(r'^affiliate/success/$', TemplateView.as_view(
            template_name="business/affiliate_form.html"
        ),
        name="affiliate-success"
    ),
    url(r'^affiliate/$', CreateView.as_view(
            form_class=FeatureForm,
            model=Feature,
            template_name="business/affiliate_form.html",
            success_url='/affiliate/success/'  # don't understand reverse('business-success')
        ),
        name="affiliate"
    ),
)
