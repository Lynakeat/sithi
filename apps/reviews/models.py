# django imports
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from activebuys.apps.companies.models import CompanyAddress
# reviews imports
from activebuys.apps.reviews.managers import ActiveManager, VoteManager
from activebuys.apps.reviews.settings import SCORE_CHOICES, VOTE_CHOICES


class Review(models.Model):
    """A ``Review`` consists on a comment and a rating.
    """
    location = models.ForeignKey(CompanyAddress, verbose_name=_(u"Location"))
    user = models.ForeignKey(User, verbose_name=_(u"User"), related_name="%(class)s_comments")
    title = models.CharField(_(u"Title"), max_length=50, blank=True,)
    comment = models.TextField(_(u"Comment"), blank=True)
    score = models.FloatField(_(u"Score"), choices=SCORE_CHOICES, default=3.0)
    active = models.BooleanField(_(u"Active"), default=False)
    creation_date = models.DateTimeField(_(u"Creation date"), auto_now_add=True)
    # ip_address  = models.IPAddressField(_(u"IP address"), blank=True, null=True)

    objects = ActiveManager()

    class Meta:
        get_latest_by = 'creation_date'
        ordering = ("-creation_date", )

    def __unicode__(self):
        return u'"%s" (%s) for %s' % (self.title, self.score, self.location.place)

    @property
    def name(self):
        """Returns the stored user name.
        """
        return self.user.get_full_name()

    @property
    def email(self):
        """Returns the stored user email.
        """
        return self.user.email

    def _votes(self):
        return self.vote_set.filter(active=True)
    votes = property(_votes)

    def type_1(self):
        return self.vote_set.filter(vote_type=1,active=True).count()

    def type_2(self):
        return self.vote_set.filter(vote_type=2,active=True).count()

    def _reviewlogs(self):       
        return self.reviewlog_set.filter().order_by('created_date')
    reviewlogs = property(_reviewlogs)


class Vote(models.Model):
    """" A ''Review'' contains of rating Useful, Funny, Cool"""
    vote_type = models.SmallIntegerField(_(u"Type"), choices=VOTE_CHOICES, blank=True)
    user = models.ForeignKey(User, verbose_name=_(u"User"), related_name='votes', blank=True, null=True)
    review = models.ForeignKey(Review, verbose_name=_(u"Review"))
    created_date = models.DateTimeField(_(u"Created date"), auto_now_add=True, editable=False)
    updated_date =  models.DateTimeField(_(u"Updated date"), auto_now_add=True, editable=False)
    ip_address = models.IPAddressField(blank=True, null=True)
    active = models.BooleanField(_(u"Active"), default=True)

    objects = VoteManager()

    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')

    def save(self, *args, **kwargs):        
        super(Vote, self).save(*args, **kwargs)


    def __unicode__(self):
        
        # Get their vote; either up or down.
        
        
        # Get the user string
        if self.user != None:
            u = "%s [%s]" % (self.user.username, self.ip_address)
        else:
            u = "[%s]" % self.ip_address
        
        return u"%s voted %s Review #%s" % (u, v, 
            self.review.id)

class ReviewLog(models.Model):
    """ Update review comment """
    review = models.ForeignKey(Review, verbose_name=_(u"Review"))
    created_date =  models.DateTimeField(_(u"Created date"), auto_now_add=True, editable=False)
    comment = models.TextField(_(u"Comment"), blank=True)
    active = models.BooleanField(_(u"Active"), default=True)

    def __unicode__(self):
        return self.comment

    def save(self, *args, **kwargs):        
        super(ReviewLog, self).save(*args, **kwargs)


    
   