from django import forms
from django.forms.util import ErrorList
from django.utils.safestring import mark_safe

class EmErrorList(ErrorList):
     def __unicode__(self):
         return self.as_em()

     def as_em(self):
         if not self: return u''
         return mark_safe(''.join([u'<em>%s</em>'%e for e in self]))

