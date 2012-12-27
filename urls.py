from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.views.generic.base import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    # apps
    #url(r'^$', 'activebuys.apps.deals.views.detail', name="home"),
    url(r'^$', 'activebuys.apps.accounts.views.registration', name="account-registration"),
    (r'^', include('activebuys.apps.companies.urls')),
    (r'^', include('activebuys.apps.business.urls')),
    (r'^zipcode/', include('activebuys.apps.zipcodes.urls')),
    (r'^widgets/', include('activebuys.apps.widget.urls')),
    (r'^deals/', include('activebuys.apps.deals.urls')),
    (r'^faq/', include('activebuys.apps.faq.urls')),
    (r'^accounts/', include('activebuys.apps.accounts.urls')),
    (r'^contacts/', include('activebuys.apps.contacts.urls')),
    (r'^review/', include('activebuys.apps.reviews.urls')),
    (r'^follow/', include('activebuys.apps.follow.urls')),
    (r'^avatar/', include('activebuys.apps.avatar.urls')),

    # static
    url('^how/$', TemplateView.as_view(template_name="how.html"), name="how"),
    url('^about/$', TemplateView.as_view(template_name="about.html"), name="about"),
    url('^terms/$', TemplateView.as_view(template_name="terms.html"), name="terms"),
    url('^policy/$', TemplateView.as_view(template_name="privacy-policy.html"), name="policy"),
    url('^universal-fine-print/$', TemplateView.as_view(template_name="universal-fine-print.html"), name="universal-fine-print"),

    # widget
    url('^widget/$', TemplateView.as_view(template_name="widget/widget.html"), name="widget"),
    url('^widget-test/$', TemplateView.as_view(template_name="widget/widget-test.html"), name="widget test"),

    # foxycart
    (r'^foxycart/cart/$', TemplateView.as_view(template_name="foxycart/cart.html")), 
    (r'^foxycart/checkout/$', TemplateView.as_view(template_name="foxycart/checkout.html")),
    (r'^foxycart/receipt/$', TemplateView.as_view(template_name="foxycart/receipt.html")),
    (r'^foxycart/datafeed/$', 'activebuys.apps.foxycart.views.datafeed'),
    (r'^foxycart/sso/$', 'activebuys.apps.foxycart.views.sso'),

    url(r'^wholefoods-popup/$', TemplateView.as_view(template_name="wholefoods-popup.html"), name="wholefoods-popup"),

    # media
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # tinymce editor
    (r'^tinymce/', include('tinymce.urls')),
)

