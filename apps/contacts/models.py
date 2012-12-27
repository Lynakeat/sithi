from django.db import models
from django.core import mail

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(blank=True, null=True, max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __unicode__(self):
        return self.subject
        
    def save(self, *args, **kwargs):
        if not self.id:
            message = ["Name: %s" % self.name,
                       "Subject: %s" % self.subject,
                       "Email: %s" % self.email,
                       "Phone: %s" % self.phone,
                       "Message:",
                       self.message
            ]
                       
            new_email = mail.EmailMessage(
                        from_email = self.email,
                        to = ['contact@activebuys.com'],
                        #bcc = ['josh@cabedge.com', 'andy@cabedge.com'],
                        subject = u"New ACTIVEBUYS Contact",
                        body = "\r\n".join(message))
            new_email.send()
        return super(Message, self).save(*args, **kwargs)

