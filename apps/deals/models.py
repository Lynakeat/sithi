from datetime import datetime, timedelta
from django.db import models
from django.core.urlresolvers import reverse
from activebuys.apps.utils.models import SortableModel

from activebuys.apps.deals.managers import ActiveDealManager, AllowedDealManager
from autoslug import AutoSlugField


# def year_from_now():


class Deal(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', editable=True, unique=True, max_length=255,)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField(db_index=True, default=datetime.now)
    end_time = models.DateTimeField(db_index=True, default=lambda:datetime.now()+timedelta(days=365))
    expire_date = models.DateField(help_text="voucher expire date", default=lambda:datetime.now()+timedelta(days=365))
    open_after_expire = models.BooleanField(default=False,
            help_text="Users could purchase deal after the deal has expired")
    total_number = models.PositiveIntegerField(default=0,
                                               help_text="0 for unlimited")
    sold = models.PositiveIntegerField(default=0)
    per_user = models.PositiveIntegerField(default=2,
                                           help_text="0 for unlimited")
    gift_limit = models.PositiveIntegerField(default=2,
                                             help_text="0 for unlimited")
    company = models.ForeignKey('companies.Company')
    nonprofit = models.ForeignKey('companies.NonProfit', blank=True, null=True)
    fine_print = models.TextField()
    background = models.ForeignKey('Background', null=True, blank=True)
    featured = models.BooleanField('Featured Deal',
                    help_text='Show this deal in "Active Deals" widgets')
    past_featured = models.BooleanField('Featured Past Deal',
                    help_text='Show this deal in featured past deals at bottom') # formerly is_featured
    allow_gifts = models.BooleanField('Allow Gifts', default=True)
    home_page = models.BooleanField(help_text='Show this deal on Home page', default=False)
    locations = models.ManyToManyField('companies.CompanyAddress')
    created = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    objects = models.Manager()
    active = ActiveDealManager() # featured deals within the publish date range
    allowed = AllowedDealManager()

    class Meta:
        ordering = ['end_time', ]

    def __unicode__(self):
        return self.title

    @property
    def discount(self):
        return int(round(self.saving / self.original_price * 100))

    @property
    def saving(self):
        return self.original_price - self.price

    def get_buy_url(self):
        return reverse('deals-buy', args=(self.slug,))

    def get_absolute_url(self):
        return reverse('deals-detail', args=(self.slug,))

    def is_closed(self):
        return datetime.now() >= self.end_time and\
               not self.open_after_expire

    def is_sold_out(self):
        return self.total_number and\
               self.sold >= self.total_number

    def first_image(self):
        photos = self.deal_photos.all()
        if photos:
            return photos[0].image.url
        return ""


class Picture(SortableModel):
    deal = models.ForeignKey(Deal, related_name="deal_photos")
    image = models.ImageField(upload_to='uploads/deals/%y/%m')

    def __unicode__(self):
        return unicode(self.deal)

    def next_sort_order(self):
        try:
            return self.deal.deal_photos.all().order_by('-sort_order')[0].sort_order + 1
        except (IndexError, AttributeError):
            return 1


class Background(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='uploads/deals-bg/%y/%m')

    def __unicode__(self):
        return self.title
