from django.db import models
from django.core import mail


class Feature(models.Model):
    BUSINESS, EMPLOYER, AFFILIATE = 'business', 'employer', 'affiliate'
    FORM_TYPE_CHOICES = (
        (BUSINESS, 'For Business'),
        (EMPLOYER, 'For Employers'),
        (AFFILIATE, 'For Affiliates')
    )

    business_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    form_type = models.CharField(default=BUSINESS, choices=FORM_TYPE_CHOICES, max_length=30)

    class Meta:
        verbose_name = 'submission'
        verbose_name_plural = 'submissions'

    def __unicode__(self):
        return self.business_name

    def save(self, *args, **kwargs):
        if not self.id:
            message = ["Business Name: %s" % self.business_name,
                       "Contact Name: %s" % self.contact_name,
                       "Email: %s" % self.email,
                       "Phone: %s" % self.phone,
                       "Website: %s" % self.website,
                       "City: %s" % self.city
            ]

            new_email = mail.EmailMessage(
                        from_email=self.email,
                        to=['info@activebuys.com', ],
                        #bcc=['josh@cabedge.com', 'andy@cabedge.com'],
                        subject=u"New ACTIVEBUYS '%s' Contact" % self.get_form_type_display(),
                        body="\r\n".join(message))
            new_email.send()
        return super(Feature, self).save(*args, **kwargs)
