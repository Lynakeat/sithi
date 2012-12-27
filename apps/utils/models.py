from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils.translation import ugettext_lazy as _

class SortableModel(models.Model):
    sort_order = models.IntegerField(_('sort order'), db_index=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['sort_order']

    def save(self, *args, **kwargs):
        if self.pk is None and self.sort_order is None:
            self.sort_order = self.next_sort_order()
        return super(SortableModel, self).save(*args, **kwargs)

    def next_sort_order(self):
        "Returns next sort_order value"
        try:
            return self.__class__.objects.all().order_by('-sort_order')[0].sort_order + 1
        except IndexError:
            return 1


class GISSortableModel(gis_models.Model):
    """ Mirror of SortableModel, but inheriting GeoDjango models.Model """
    sort_order = models.IntegerField(_('sort order'), db_index=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['sort_order']

    def save(self, *args, **kwargs):
        if self.pk is None and self.sort_order is None:
            self.sort_order = self.next_sort_order()
        return super(GISSortableModel, self).save(*args, **kwargs)

    def next_sort_order(self):
        "Returns next sort_order value"
        try:
            return self.__class__.objects.all().order_by('-sort_order')[0].sort_order + 1
        except IndexError:
            return 1