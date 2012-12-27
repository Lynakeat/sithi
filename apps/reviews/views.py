# django imports
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms.util import ErrorList
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView

# reviews imports
import activebuys.apps.reviews.signals
from activebuys.apps.reviews import utils as reviews_utils
from activebuys.apps.reviews.forms import ReviewAddForm, update_review_log
from activebuys.apps.reviews.models import Review, Vote, ReviewLog
from activebuys.apps.reviews.settings import SCORE_CHOICES, VOTE_CHOICES

from datetime import datetime

from activebuys.apps.companies.models import CompanyAddress as Location
from django.utils import simplejson


class CreateReviewForObjectView(CreateView):
    """ View for creating a Review for a particular Location(CompanyAddress)
    User can only create one review per Location.
    Reviews not available for Locations whose Company has `enable_reviews=False`

    TODO: refactor get(), put() methods
    
    """
    model = Review
    form_class = ReviewAddForm

    def get(self, request, *args, **kwargs):
        """ Infer Location from 'pk' URL argument. 
        - 404 if not found, or if reviews are not enabled for that Location's company
        - Redirect to 'already reviewed' page if necessary
        - else, process form view as is
        """
        self.location = get_object_or_404(Location, id=kwargs['pk'])
        if not self.location.company.enable_reviews:
            return HttpResponseRedirect(reverse('reviews_disabled'))
        self.user = request.user
        if Review.objects.filter(user=self.user, location=self.location).count() > 0:
            return HttpResponseRedirect(reverse('reviews_already_rated'))
        return super(CreateReviewForObjectView, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ Infer Location from 'pk' URL argument. 
        - 404 if not found, or if reviews are not enabled for that Location's company
        - Redirect to 'already reviewed' page if necessary
        - else, process form view as is
        """
        self.location = get_object_or_404(Location, id=kwargs['pk'])
        if not self.location.company.enable_reviews:
            return HttpResponseRedirect(reverse('reviews_disabled'))
        self.user = request.user
        if Review.objects.filter(user=self.user, location=self.location).count() > 0:
            return HttpResponseRedirect(reverse('reviews_already_rated'))
        return super(CreateReviewForObjectView, self).post(self, request, *args, **kwargs)

    def get_success_url(self):
        return reverse("reviews_thank_you") # return to Location detail page?

    def get_context_data(self, **kwargs):
        context = super(CreateReviewForObjectView, self).get_context_data(**kwargs)
        context['object'] = self.location
        return context

    def get_form_kwargs(self, **kwargs):
        kwargs = super(CreateReviewForObjectView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'location': self.location,
            'user': self.user,
        })
        return kwargs


def add_form(request, content_id, template_name="reviews/review_form.html"):
    """Displays the form to add a review. Dispatches the POST request of the 
    form to save or reedit.
    """
    object = get_object_or_404(Location, pk=content_id)

    if reviews_utils.has_rated(request, object):
        return HttpResponseRedirect(reverse("reviews_already_rated"))

    scores = []
    for i, score in enumerate(SCORE_CHOICES):
        scores.append({
            "title": score[0],
            "value" : score[0],
            "z_index" : 10-i,
            "width" : (i+1) * 25,
        })

    if request.method == "POST":
        form = ReviewAddForm(data=request.POST)
        # "Attach" the request to the form instance in order to get the user
        # out of the request within the clean method of the form (see above).
        form.request = request
        if form.is_valid():
            if settings.REVIEWS_SHOW_PREVIEW:
                return preview(request)
            else:
                # form.user = request.user
                # form.location = object
                return save(request)
    else:
        form = ReviewAddForm()

    return render_to_response(template_name, RequestContext(request, {
        "content_id" : content_id,
        "object" : object,
        "form" : form,
        "scores" : scores,
        "show_preview" : settings.REVIEWS_SHOW_PREVIEW,
    }))

def reedit(request, template_name="reviews/review_form.html"):
    """Displays a form to edit a review. This is used if a reviewer re-edits
    a review after she has previewed it.
    """
    # get object
    object = Location.objects.get(pk=content_id)

    if reviews_utils.has_rated(request, object):
        return HttpResponseRedirect(reverse("reviews_already_rated"))

    scores = []
    for i, score in enumerate(SCORE_CHOICES):
        scores.append({
            "title": score[0],
            "value" : score[0],
            "current" : str(score[0]) == request.POST.get("score"),
            "z_index" : 10-i,
            "width" : (i+1) * 25,
        })

    form = ReviewAddForm(data=request.POST)
    return render_to_response(template_name, RequestContext(request, {
        "content_id" : content_id,
        "form" : form,
        "scores" : scores,
        "object" : object,
        "show_preview" : settings.REVIEWS_SHOW_PREVIEW,
    }))

def reedit_or_save(request):
    """Edits or saves a review dependend on which button has been pressed.
    """
    if request.POST.get("edit"):
        return reedit(request)
    else:
        return save(request)

def save(request):
    """Saves a review.
    """
    form = ReviewAddForm(data=request.POST)
    form.request = request
    if form.is_valid():
        new_review = form.save(commit=False)
        # save Location ref
        new_review.location = Location.objects.get(pk=form.cleaned_data['content_id'])
        # new_review.session_id = request.session.session_key
        # new_review.ip_address = request.META.get("REMOTE_ADDR")
        if request.user.is_authenticated():
            new_review.user = request.user
        new_review.active = not settings.REVIEWS_IS_MODERATED
        new_review.save()

        # Fire up signal
        reviews.signals.review_added.send(new_review)

        # Save object within session
        # ctype = ContentType.objects.get_for_id(new_review.content_type_id)
        # object = ctype.get_object_for_this_type(pk=new_review.content_id)
        request.session["last-rated-object"] = object

        return HttpResponseRedirect(reverse("reviews_thank_you"))

def preview(request, template_name="reviews/review_preview.html"):
    """Displays a preview of the review.
    """
    content_id = request.POST.get("content_id")
    object = Location.objects.get(pk=content_id)

    name = request.user.get_full_name()
    email = request.user.email

    return render_to_response(template_name, RequestContext(request, {
        "score" : float(request.POST.get("score", 0)),
        "object" : object,
        "name" : name,
        "email" : email,
    }))

def thank_you(request, template_name="reviews/thank_you.html"):
    """Displays a thank you page.
    """
    if request.session.has_key("last-rated-object"):
        object = request.session.get("last-rated-object")
        del request.session["last-rated-object"]
    else:
        object = None

    return render_to_response(template_name, RequestContext(request, {
        "object" : object,
    }))

def already_rated(request, template_name="reviews/already_rated.html"):
    """Displays a alreday rated page.
    """
    return render_to_response(template_name, RequestContext(request))


def vote_review(request):
    if request.method == 'POST':
        
        review_id = int(request.POST.get("id"))
        vote_type = int(request.POST.get("type"))

        review = get_object_or_404(Review, pk=review_id)     
        ip_address = reviews_utils.get_client_ip(request)             
        
        try:
            if request.user.is_authenticated():
                vote_user = request.user
                Vote.objects.get(vote_type=vote_type, user=vote_user, review=review, active=True)
            else:
                Vote.objects.get(vote_type=vote_type, ip_address=ip_address, review=review, active=True)

        except Vote.DoesNotExist:            
            # No vote exists
            try:
                if request.user.is_authenticated():
                    vote_user = request.user
                    Vote.objects.get(user=vote_user, review=review, active=True)
                else:
                    Vote.objects.get(ip_address=ip_address, review=review, active=True) 
            except Vote.DoesNotExist:  
                if request.user.is_authenticated():
                    vote_user = request.user
                    Vote.objects.create(vote_type=vote_type, user=vote_user, ip_address=ip_address, review=review)
                else:
                    Vote.objects.create(vote_type=vote_type, ip_address=ip_address, review=review)
            else:
                if request.user.is_authenticated():
                    obj = Vote.objects.get(user=request.user, review=review,active=True)  
                else:
                    obj =  Vote.objects.get(ip_address=ip_address, review=review,active=True) 
                obj.vote_type = vote_type       
                obj.save()  

        else:
            if request.user.is_authenticated():
                obj = Vote.objects.get(vote_type=vote_type, user=request.user, ip_address=ip_address, review=review,active=True)  
            else:
                obj =  Vote.objects.get(vote_type=vote_type, ip_address=ip_address, review=review,active=True) 

            obj.active = False         
            obj.save()

        result = []
        for i, vtype in enumerate(VOTE_CHOICES):
            result.append({
                "name": vtype[0],
                "value" : Vote.objects.filter(vote_type=vtype[0], review=review, active=True).count(),
            })
           
        return HttpResponse(simplejson.dumps(result), mimetype="application/json")

DATETIME_FORMAT = '%B %d, %Y, %H:%M %p'
def update_review(request):
    """ ajax profile editting """
    if request.method == 'POST':        
        review_id = int(request.POST.get("review_id"))
        comment = request.POST.get("comment")

        review = get_object_or_404(Review, pk=review_id)   

        if review.user.id == request.user.id:
            ReviewLog.objects.create(comment=comment, review=review)

        
        log = ReviewLog.objects.filter(review=review).order_by('-created_date')[0]
        result = []
        result.append({
                "comment": log.comment,
                "created_date" : log.created_date.strftime(DATETIME_FORMAT)
            })
        return HttpResponse(simplejson.dumps(result), mimetype="application/json")


