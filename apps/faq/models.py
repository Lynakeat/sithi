from django.db import models
from activebuys.apps.utils.models import SortableModel


class FAQ(SortableModel):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    
    def __unicode__(self):
        return self.question

