from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from activebuys.apps.reviews.views import CreateReviewForObjectView

urlpatterns = patterns('activebuys.apps.reviews.views',
    url(r'^add/(?P<pk>\d*)/$', login_required(CreateReviewForObjectView.as_view()), name="reviews_add"),
    # url(r'^preview$', "preview", name="reviews_preview"),
    # url(r'^reedit$', "reedit_or_save", name="reviews_reedit"),
    url(r'^thank-you$', "thank_you", name="reviews_thank_you"),
    url(r'^disabled$', TemplateView.as_view(template_name='reviews/disabled.html'), name="reviews_disabled"),
    url(r'^already-reviewed$', "already_rated", name="reviews_already_rated"),
    url(r'^vote-review$', "vote_review", name="vote_add"),
    url(r'^update$', "update_review", name="update_review"),
)
