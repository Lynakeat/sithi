# django imports
from django.contrib import admin

# lfs imports
from activebuys.apps.reviews.models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title','score','active','user','creation_date','location']
    list_display_links = ['title','score']
    list_filter = ['score','active','creation_date']
    search_fields = ['location__place','title','user__email','user__username']
    raw_id_fields = ['location','user']

admin.site.register(Review, ReviewAdmin)