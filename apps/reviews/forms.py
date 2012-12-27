from django.conf import settings
from django import forms
from django.forms import ModelForm

from activebuys.apps.reviews.models import Review, Vote, ReviewLog


class ReviewAddForm(ModelForm):
    """Form to add a review. Requires that a `user` and `location` reference
    also be saved in addition to the included fields.
    """
    terms_agreed = forms.BooleanField(required=True,label='Agree to Terms')

    class Meta:
        model = Review
        fields = ("title", "comment", "score")

    def __init__(self, user, location, *args, **kwargs):
        # self.user = kwargs['initial']['user']
        # self.location = kwargs['initial']['location']
        self.user = user
        self.location = location
        super(ReviewAddForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['title','score','comment','terms_agreed']
        self.fields['score'].label = 'How Many Stars?'
        # self.fields['score'].empty_value = 'Choose:'
        self.fields['comment'].required = True

    def save(self, commit=True):
        obj = super(ReviewAddForm, self).save(False)
        obj.user = self.user
        obj.location = self.location
        obj.active = not settings.REVIEWS_IS_MODERATED
        commit and obj.save()
        return obj

def update_review_log(fields):
    fields.remove('csrfmiddlewaretoken')
    class FormClass(forms.ModelForm):
        class Meta:
            model = ReviewLog
            fields = ("comment")

        def __init__(self, *args, **kwargs):
            super(FormClass, self).__init__(*args, **kwargs)        

        def save(self, commit=True):
            inst = super(FormClass, self).save(commit=False)
            if commit:
                inst.save()
            return inst
    return FormClass