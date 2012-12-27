from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, RedirectView

from activebuys.apps.companies.models import Category, SubCategory, CompanyAddress, DAYS_OF_WEEK
from activebuys.apps.deals.models import Deal
from activebuys.apps.reviews.models import Review
from activebuys.apps.zipcodes.forms import ZipCodeForm
from activebuys.apps.zipcodes.models import ZipCode

import refinery


class LocationFilterTool(refinery.FilterTool):
    """ FilterTool customized to accept a 'category' paremeter and limit the 
    'subcategories' filter to SubCategory instances related to that Category.
    Also override the label for that filter.

    """
    class Meta:
        model = CompanyAddress
        fields = ['subcategories']
        # order_by = ('distance', 'place', 'subcategories__name', '-avg_rating')
        order_by = (
            ('distance', 'Nearest'),
            ('place', 'Name'),
            ('subcategories__name', 'Subcategory'),
            # ('-avg_rating', 'Highest Rated'), # -total_reviews
        )

    def __init__(self, *args, **kwargs):
         # store category to limit filters to
        self.category = kwargs.pop('category')
        super(LocationFilterTool, self).__init__(*args, **kwargs)
        self.filters['subcategories'].label = u'Filter by:'
        self.filters['subcategories'].extra.update({
                'queryset': SubCategory.objects.filter(category=self.category)
            })

    def get_ordering_field(self):
        if self._meta.order_by:
            if isinstance(self._meta.order_by, (list, tuple)):
                # choices = [(f, capfirst(f)) for f in self._meta.order_by]
                if isinstance(self._meta.order_by[0], (list, tuple)):
                    choices = [(f[0], f[1]) for f in self._meta.order_by]
                else:
                    choices = [(f, capfirst(f)) for f in self._meta.order_by]
            else:
                # choices = [(f, capfirst(f)) for f in self.filters]
                choices = [(f, fltr.label) for f, fltr in self.filters.items()]
            return forms.ChoiceField(label="Sort by:", required=False, choices=choices)


class CategoryListView(ListView):
    """ Provide a list of all the Categories as `object_list`

    Additional context:
     - `featured_location`: 1 featured CompanyAddress
     - `highest_rated`: top 2 CompanyAddress instances by average Review score 
     - `latest_review`: most recent "active" Review 

    """
    model = Category
    allow_empty = True

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CategoryListView, self).get_context_data(**kwargs)

        if not 'zip_code' in self.request.session.keys():
            self.request.session['zip_code'] = ZipCode.objects.get(code='37201')
        context['zipcode_form'] = ZipCodeForm(initial={'zip_code': self.request.session['zip_code'].code})
        # Add featured location
        try:
            context['featured_location'] = CompanyAddress.objects.filter(featured=True)[0]
        except IndexError:
            context['featured_location'] = None
        # Add 2 highest rated locations:
        #  - only for locations that have reviews (not "None")
        #  - only for 'active' reviews
        #  - only for locations whose Company has 'enable_reviews=True'
        #  - additionally sorted by highest number of ratings, all things equal
        context['highest_rated'] = CompanyAddress.objects.filter(review__active=True, review__location__company__enable_reviews=True)\
            .annotate(avg_rating=Avg('review__score'), total_ratings=Count('review'))\
            .order_by('-avg_rating','-total_ratings')[:2]
        # Add latest review
        #  - only for 'active' reviews
        try:
            context['latest_review'] = Review.objects.active().latest()
        except ObjectDoesNotExist:
            context['latest_review'] = None
        return context


class LocationListView(ListView):
    """ List of CompanyAddress instances as `object_list`:
     - for a particular Category (identified by slug)
     - sorted by proximity to a given ZIP code

    Additional context:
     - `category`: the Category instance identified by the slug in the URL
     - `categories`: list of all available Category instances
     - `featured_location`:
            - if not filtered: 'featured_location' of Category
            - if filtered: highest rated of results
     - `zipcode`: the ZipCode instance used to order the list by proximity
     - `zipcode_form`: form instance for modifying the session's ZIP code
     - `filtertool`: FilterTool instance

    """

    allow_empty = True
    template_name = "companies/location_list.html"
    paginate_by = 10

    def get_queryset(self):
        """
        In addition to returning a modified queryset based on the 
        LocationFilterTool's filtering, also set the featured location:
         - if not filtered, use category's featured location
         - if filtered, use the first result

        """
        self.category = get_object_or_404(Category, slug__exact=self.kwargs['slug'])

        # if no ZIP code in session, set one for a central Nashville ZIP code
        if not 'zip_code' in self.request.session.keys():
            self.request.session['zip_code'] = ZipCode.objects.get(code='37201')

        # filter to current category
        qs = CompanyAddress.objects.filter(categories=self.category)
        # find distance for each records in queryset
        qs = qs.distance(self.request.session['zip_code'].geometry, field_name='point')
        # include average rating for each
        qs = qs.annotate(avg_rating=Avg('review__score'), total_reviews=Count('review'))
        # sort by that distance
        qs = qs.order_by('distance') #.distinct() # and make sure there are no duplicates
        # build the filter, save to instance
        self.locations_filter = LocationFilterTool(self.request.GET, queryset=qs, category=self.category)
        # determine if filtering is in use
        if self.locations_filter.qs.count() == qs.count():
            # if no, return filter's full queryset
            # use category's featured location, include its distance to session zipcode
            try:
                self.featured_location = CompanyAddress.objects.filter(category=self.category).distance(self.request.session['zip_code'].geometry)[0]
            except IndexError:
                self.featured_location = None
        else:
            # if yes, return highest rated (tie breaker: most rated) CompanyAddress
            try:
                self.featured_location = self.locations_filter.qs.filter(review__score__isnull=False).order_by('-avg_rating','-total_reviews')[0]
                # tell the template that this is selected by rating
                self.featured_location.favorite = True
            except IndexError:
                self.featured_location = None
        return self.locations_filter.qs

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LocationListView, self).get_context_data(**kwargs)
        context['featured_location'] = self.featured_location
        context['category'] = self.category
        context['categories'] = Category._default_manager.all()
        if not 'zip_code' in self.request.session.keys():
            self.request.session['zip_code'] = ZipCode.objects.get(code='37201')
        context['zipcode_form'] = ZipCodeForm(initial={'zip_code': self.request.session['zip_code'].code})
        context['filtertool'] = self.locations_filter
        return context


class LocationDetailView(DetailView):
    """ Detail view with Location(CompanyAddress) as `object`.

    Additional context:
     - `already_reviewed`: boolean - whether a User has reviewed the Location
     - `categories`: list of all available Category instances
     - `days`: the DAYS_OF_WEEK setting from the models module, for reference
     - `show_all`: True - tells shared template to display additional info
     
    """
    # model = CompanyAddress
    template_name = "companies/location_detail.html"

    def get_queryset(self):
        # if no ZIP code in session, set one for a central Nashville ZIP code
        if not 'zip_code' in self.request.session.keys():
            self.request.session['zip_code'] = ZipCode.objects.get(code='37201')
        return CompanyAddress.objects.all().distance(self.request.session['zip_code'].geometry, field_name='point')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LocationDetailView, self).get_context_data(**kwargs)
        # Determine whether user has reviewed the Location
        if self.request.user.is_authenticated():
            already_reviewed = Review.objects.filter(user=self.request.user, location=self.object).count() > 0
        else:
            already_reviewed = False
        context['already_reviewed'] = already_reviewed
        context['categories'] = Category._default_manager.all()
        context['days'] = DAYS_OF_WEEK
        context['show_all'] = True 
        if not 'zip_code' in self.request.session.keys():
            self.request.session['zip_code'] = ZipCode.objects.get(code='37201')

        context['zipcode_form'] = ZipCodeForm(initial={'zip_code': self.request.session['zip_code'].code})
        return context


class LocationRedirectView(RedirectView):
    """ Redirects requests for a Location(CompanyAddress) using the pk, to the 
    corresponding URL based on the Location's slug.
    """
    permanent = True
    
    def get_redirect_url(self, **kwargs):
        location = get_object_or_404(CompanyAddress, pk=kwargs['pk'])
        return location.get_absolute_url()