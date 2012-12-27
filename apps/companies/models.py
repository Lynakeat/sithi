import re
import urllib
from datetime import datetime
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.contrib.localflavor.us.models import USStateField
from django.db import models
from django.db.models import Avg
from geopy import geocoders
from activebuys.apps.utils.models import SortableModel, GISSortableModel
from autoslug import AutoSlugField
from activebuys.apps.follow import utils

GEOCODER = geocoders.Google()

class BaseCompany(SortableModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to='uploads/companies/%y/%m', 
                             blank=True, null=True, 
                             help_text="180 x 140")
    website = models.URLField()

    class Meta:
        abstract = True
        ordering = ['sort_order',]

    def __unicode__(self):
        return self.name


class NonProfit(BaseCompany):
    featured = models.BooleanField(default=False)


class Company(BaseCompany):
    """ Groups Location (CompanyAddress) instances together. """
    is_partner = models.BooleanField(default=False, verbose_name='partner')
    enable_products = models.BooleanField(default=False,)
    enable_reviews = models.BooleanField(default=False,)
    enable_courses = models.BooleanField(default=False,)
    enable_pricing = models.BooleanField(default=False,)
    notification_email = models.EmailField(null=True, blank=True, 
                                verbose_name='email', 
                                help_text='email address for notifications')

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'


class Category(models.Model):
    """ Top-level categorization for CompanyAddress instances """
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    featured_location = models.ForeignKey('CompanyAddress', null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('resources-location-list', (), {
            'slug': self.slug,
            })


class SubCategory(models.Model):
    """ Second-level categorization for CompanyAddress instances """
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    class Meta:
        ordering = ['name']
        verbose_name = 'sub-category'
        verbose_name_plural = 'sub-categories'

    def __unicode__(self):
        return self.name


class CompanyAddress(GISSortableModel):
    """ Location, perhaps of a franchise """
    company = models.ForeignKey(Company)
    place = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='place', editable=True, unique=True,
                         max_length=255)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = USStateField(default='TN')
    postal_code = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    fax = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='uploads/locations/%y/%m', 
                             blank=True, null=True, 
                             help_text="180 x 140")
    website = models.URLField(blank=True, null=True)
    facebook_profile = models.URLField(blank=True, null=True)
    hours = models.TextField(blank=True, null=True)
    email = models.EmailField(null=True, blank=True, help_text='email address for `mailto:` link')
    categories = models.ManyToManyField(Category, null=True, blank=True)
    subcategories = models.ManyToManyField(SubCategory, null=True, blank=True)
    point = gis_models.PointField(srid=4326, null=True, blank=True, verbose_name='GIS point') # srid compatible with Google Maps
    featured = models.BooleanField(default=False)

    objects = gis_models.GeoManager()

    class Meta:
        verbose_name = 'location'
        verbose_name_plural = 'locations'

    def __unicode__(self):
        return self.place

    @models.permalink
    def get_absolute_url(self):
        return ('resources-location-detail', (), {
            'slug': self.slug,
            })

    def _reviews(self):
        return self.review_set.filter(active=True)
    reviews = property(_reviews)

    def average_rating(self):
        return self.review_set.filter(active=True).aggregate(Avg('score'))['score__avg']

    def total_reviews(self):
        return self.review_set.filter(active=True).count()

    def active_deals(self):
        return self.deal_set.filter(end_time__gte=datetime.now(), start_time__lte=datetime.now())

    def map_it(self):
        """ Return Google map URL using address, city, state """
        return "http://maps.google.com?q=%(address)s,%(city)s,%(state)s" %{
            'address': self.address,
            'city': self.city,
            'state': self.state,
        }

    @property
    def full_address(self):
        if self.postal_code:
            return u"%s, %s, %s %s" % (self.address, self.city, self.state, self.postal_code)
        else:
            return u"%s, %s, %s" % (self.address, self.city, self.state)
        
    def geocode_address(self):
        # use a geocoding service to return a Point from the full address
        try:
            place, (lat, lng) = GEOCODER.geocode(self.full_address)
            return Point(float(lng), float(lat))
        except ValueError: # also, geopy.geocoders.google.GQueryError and others
            pass
        return None
    
    def save(self, geocode=True, *args, **kwargs):
        """ Re-saves the location any time saved"""
        if geocode:
            self.point = self.geocode_address()
        super(CompanyAddress, self).save(*args, **kwargs)
        
utils.register(CompanyAddress)

class Course(models.Model):
    """ A class/course provided by a company that a user might attend. """
    location = models.ForeignKey(CompanyAddress)
    title = models.CharField(max_length=200)
    duration = models.CharField(max_length=50, null=True, blank=True)
    audience = models.CharField(max_length=50, null=True, blank=True)
    note = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        ordering = ['title']
        verbose_name='class'
        verbose_name_plural='classes'

    def __unicode__(self):
        return self.title


DAYS_OF_WEEK = (
    (0, 'Sunday'),
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
)


class StartTime(models.Model):
    """ Time a Course/Class begins, on a certain day of the week. """
    course = models.ForeignKey(Course, verbose_name='class')
    day_of_week = models.PositiveIntegerField(choices=DAYS_OF_WEEK, verbose_name='day of week')
    time = models.TimeField()

    class Meta:
        ordering = ['day_of_week', 'time']
        verbose_name = 'start time'
        verbose_name_plural = 'start times'

    def __unicode__(self):
        return u'%s on %s' % (self.time, self.day_of_week)


class Product(models.Model):
    """ Product offered by a Location (CompanyAddress) """
    location = models.ForeignKey(CompanyAddress)
    title = models.CharField(max_length=50)
    brands = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __unicode__(self):
        return self.title


class LocationPhoto(SortableModel):
    location = models.ForeignKey(CompanyAddress)
    image = models.ImageField(upload_to='uploads/locations/photos/%y/%m')

    class Meta:
        ordering = ['sort_order',]

    def __unicode__(self):
        return u'photo for %s' % self.location.place
