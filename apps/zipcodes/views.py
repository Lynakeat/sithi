from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.functional import lazy
from django.views.generic import FormView

from activebuys.apps.zipcodes.forms import ZipCodeForm
from activebuys.apps.zipcodes.models import ZipCode

# Workaround for using reverse with success_url in class based generic views
# because direct usage of it throws an exception.
# http://djangosnippets.org/snippets/2445/
# Django 1.4 removes need for this: https://docs.djangoproject.com/en/dev/releases/1.4/#reverse-lazy
reverse_lazy = lambda name=None, *args : lazy(reverse, str)(name, args=args)


class SaveZipCodeToSessionView(FormView):
    """ Save ZipCode instance to session, and redirect to page user was previously on """
    form_class = ZipCodeForm
    success_url = reverse_lazy('zipcode_success')
    template_name = 'zipcodes/form.html'

    # def get_initial(self):
    #     # if zipcode is in the session, use it
    #     return {'zip_code': '55555'}

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        # save new zipcode to session
        if form.is_valid():
            self.request.session['zip_code'] = form.cleaned_data['zip_code']
            return self.form_valid(form)
        else:
            return self.form_invalid(form)