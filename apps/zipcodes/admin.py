from django import forms
from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin, OSMGeoAdmin

from activebuys.apps.zipcodes.models import ZipCode

class ZipCodeAdmin(GeoModelAdmin):
    # exclude = ('map_url','geometry')
    # list_display = ['name', 'state', 'zip_code'] # product_lines
    # list_filter = ('product_lines',)
    
    default_lon = -86.78
    default_lat = 36.17
    
#    def formfield_for_dbfield(self, db_field, **kwargs):
#        if db_field.name == 'zip_code':
#            return forms.CharField(widget=forms.TextInput(
#                attrs={'maxlength': 5,}
#            ))
#        return super(LocationAdmin, self).formfield_for_dbfield(db_field, **kwargs)

#    def save_model(self, request, obj, form, change):
#        obj.zip_code = ZipCode.objects.get(code=form.cleaned_data['zip_code'])
#        obj.save()

#    def clean_zip_code(self):
#        raise Exception('clean method reached')

    
admin.site.register(ZipCode, ZipCodeAdmin)
