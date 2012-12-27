from django.contrib import admin
from activebuys.apps.business.models import Feature


class FeatureAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'contact_name', 'email', 'phone', 'website', 'city', 'form_type']
    list_filter = ['form_type', ]


admin.site.register(Feature, FeatureAdmin)
