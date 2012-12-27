from django.contrib.gis.db import models
from django.contrib.localflavor.us.models import USStateField


class ZipCode(models.Model):
    """
    A US postal code, including a center point.  This can be used to find 
    approximate distances to other GIS geometry.
    
    """
    code = models.CharField(max_length=5) # some codes contain letters, like H and X
    geometry = models.PointField(srid=4326, null=True, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = USStateField(blank=True)    
    
    objects = models.GeoManager()
    
    class Meta:
        verbose_name = 'ZIP code'
        verbose_name_plural = 'ZIP codes'

    def __unicode__(self):
        if self.city and self.state:
            return '%s (%s, %s)' % (self.code, self.city, self.state)
        else:
            return self.code
