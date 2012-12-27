import hashlib
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.localflavor.us.models import USStateField

from activebuys.apps.foxycart import Cart
from activebuys.apps.companies.models import Category

FEMALE, MALE = 'F', 'M'
GENDER_CHOICES = (
    (FEMALE, 'Female'),
    (MALE, 'Male')
)

BEGINNER, INTERMEDIATE, EXPERT, MASTER = 'B', 'I', 'E', 'M'
LEVEL_CHOICES = (
    (BEGINNER, 'Beginner'),
    (INTERMEDIATE, 'Intermediate'),
    (EXPERT, 'Expert'),
    (MASTER, 'Master')
)


class SubscribeLocation(models.Model):
    name = models.CharField(max_length=150)
    cmonitor_name = models.CharField(max_length=150, verbose_name="CM name",
                                     help_text="This must be exact name of city option in campaign monitor")

    def __unicode__(self):
        return self.name


class Account(User):
    subscribe_location = models.ManyToManyField(SubscribeLocation)
    referred_email = models.CharField(max_length=255, blank=True, null=True)
    confirm_email_code = models.CharField(max_length=255, blank=True, editable=False)
    foxycart_customer_id = models.IntegerField(null=True)    
    gender = models.CharField(default='', choices=GENDER_CHOICES, max_length=3)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = USStateField(blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    interests = models.ManyToManyField(Category)
    about_me = models.TextField(blank=True, null=True)
    active_level = models.CharField(default='', choices=LEVEL_CHOICES, max_length=3)


    def get_restore_pass_code(self):
        return self.restorepasswordrequest_set.latest('timestamp').code

    @property
    def full_location(self):
        return u"%s, %s, %s" % (self.address, self.city, self.state)

class AccountDealManager(models.Manager):
    def active(self):
        """ Paid and used deals are active """
        return self.get_query_set().exclude(status=AccountDeal.NEW)

    def all_new(self):
        return self.get_query_set().filter(status=AccountDeal.NEW)


class AccountDeal(models.Model):
    PAID, NEW, USED = 'paid', 'new', 'used'
    STATUS_CHOICES = (
        (PAID, 'Paid'),
        (NEW, 'New'),
        (USED, 'Used')
    )
    status = models.CharField(default=NEW, choices=STATUS_CHOICES, max_length=10)
    account = models.ForeignKey(Account)
    deal = models.ForeignKey('deals.Deal')
    location = models.ForeignKey('companies.CompanyAddress')
    nonprofit = models.ForeignKey('companies.NonProfit', blank=True, null=True)
    is_gift = models.BooleanField(default=False)
    name_to = models.CharField(max_length=255, blank=True, null=True)  # required if is_gift == True
    name_from = models.CharField(max_length=255, blank=True, null=True)  # required if is_gift == True
    message = models.TextField(blank=True, null=True)  # required if is_gift == True
    surprise = models.BooleanField(default=False)
    email_to = models.EmailField(blank=True, null=True)  # required if is_gift == True
    timestamp = models.DateTimeField(auto_now_add=True)
    fcc_session_id = models.CharField(max_length=255)  # need for add/remove items from foxycart
    widget_id = models.CharField(max_length=255, blank=True)

    objects = AccountDealManager()

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return u"#%d %s %s" % (self.id, self.deal, self.account)

    @property
    def is_paid(self):
        return self.status == AccountDeal.PAID

    @property
    def is_used(self):
        return self.status == AccountDeal.USED

    @classmethod
    def clean_by_fcid(cls, fcc_session_id):
        """ remove all items from cart """
        if '&fcsid=' not in fcc_session_id:
            fcc_session_id = '&fcsid=' + fcc_session_id
        cls.objects.all_new().filter(fcc_session_id=fcc_session_id).delete()
        cart = Cart(fcc_session_id)
        cart.clean_cart()


class Order(models.Model):
    date = models.DateTimeField()
    transaction_id = models.BigIntegerField(max_length=255)
    account = models.ForeignKey(Account)
    deals = models.ManyToManyField(AccountDeal)
    total = models.FloatField()
    receipt_url = models.URLField()

    def __unicode__(self):
        return str(self.id)

    def get_gifts(self):
        """ return gifts grouped by email """
        output = {}
        # regroup by recepients
        for deal in self.deals.filter(is_gift=True, surprise=False):
            if isinstance(output.get(deal.email_to), dict):
                output[deal.email_to]['deals'].append(deal)
            else:
                output[deal.email_to] = {
                    'deals': [deal],
                    'name_to': deal.name_to,
                    'name_from': deal.name_from
                }
        return output


class Data(models.Model):
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class RestorePasswordRequest(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account)
    code = models.CharField(max_length=255, blank=True, editable=False)

    def save(self, *args, **kwargs):
        super(RestorePasswordRequest, self).save(*args, **kwargs)
        if not self.code:
            salt = unicode(self.timestamp)
            self.code = hashlib.sha224(settings.SECRET_KEY + salt + self.account.email + self.account.username).hexdigest()
            self.save()


@receiver(models.signals.post_save, sender=AccountDeal, dispatch_uid="save_accountdeal")
def save_accountdeal(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs['created'] and not kwargs['raw'] == True: # 'raw' flag is for when loaddata is running
        # add deal to foxycart
        cart = Cart(instance.fcc_session_id)
        cart.add_to_cart(instance)


@receiver(models.signals.post_delete, sender=AccountDeal, dispatch_uid="remove_accountdeal")
def remove_accountdeal(sender, **kwargs):
    instance = kwargs['instance']
    # remove deal from foxycart
    count = instance.account.accountdeal_set.all_new().\
                             filter(deal=instance.deal).\
                             exclude(id=instance.id).\
                             count()
    cart = Cart(instance.fcc_session_id)
    cart.update_cart(instance, count)


@receiver(models.signals.post_save, sender=AccountDeal, dispatch_uid="increase_sold")
def increase_sold(sender, **kwargs):
    instance = kwargs['instance']
    if instance.is_paid and not kwargs['raw'] == True: # 'raw' flag is for when loaddata is running
        # recalculate sold deals
        instance.deal.sold = instance.deal.accountdeal_set.active().count()
        instance.deal.price = str(instance.deal.price)  # fixing this issue ? https://code.djangoproject.com/ticket/10933
        instance.deal.save()
