from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView

urlpatterns = patterns('activebuys.apps.accounts.views',   
    url(r'^purchase/$', 'purchase', name="account-purchase"),
    url(r'^review/$', 'review', name="account-review"),
    url(r'^resource/$', 'follow', name="account-resource"),    
    url(r'^resource/(?P<slug>[-\w]+)/$', 'resource_subcategory', name="account-resource-subcategory"),
    url(r'^profile/view/(?P<id>[-\w]+)/$', 'profile_view', name="account-profile-view"),
    
    url(r'^profile/$', 'profile', name="account-profile"),
    url(r'^profile/edit/$', 'profile_edit', name="account-profile-edit"),
    url(r'^profile/mark-deal-as-used/$', 'mark_as_used', name="account-deal-mark-as-used"),
    url(r'^profile/resend-gift/$', 'resend_gift', name="account-resend-gift"),
    url(r'^registration/$', 'registration', name="account-registration"),
    url(r'^login/$', 'login', name="account-login"),
    url(r'^confirm/$', 'confirm', name="account-confirm"),
    url(r'^restore-password/$', 'restore_password', name="account-restore-password"),
    url(r'^resend-confirmation/$', 'resend_confirmation', name="account-resend-confirmation"),
    url(r'^send-restore-code/$', 'send_restore_code', name="account-send-restore-code"),
    url(r'^remove_accountdeal/$', 'remove_accountdeal', name="remove_accountdeal"),
) + patterns('django.contrib.auth.views',
    url(r'^logout/$', 'logout', {'next_page':"/"}, name="account-logout"),
) + patterns('',
    url(r'^registration/refer-popup/$',
        TemplateView.as_view(template_name="accounts/refer-popup.html"),
        name="registration-refer-popup"
    ),    
)
