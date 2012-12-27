from django import forms
from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from django.db import models
from django.forms.models import BaseInlineFormSet

from activebuys.apps.companies.models import Company, NonProfit, Product, \
        CompanyAddress, Category, SubCategory, Course, StartTime, LocationPhoto
from activebuys.apps.companies.forms import NonProfitForm, CompanyAdminForm
from activebuys.apps.companies import admin_views
from activebuys.apps.deals.models import Deal
from activebuys.apps.utils.admin import ImgPreview


class MarkitUpMedia:
    js = (
        'js/jquery-1.6.1.min.js',
        'js/markitup/jquery.markitup.pack.js',
        'js/markitup/sets/markdown/set.js',
        'js/markitup_admin.js',
    )
    css = {
        'all': (
            'js/markitup/skins/simple/style.css',
            'js/markitup/sets/markdown/style.css',
        )
    }


class TabularInlineWithEditLink(admin.TabularInline):
    """ Inline that provides an "edit" link to the inlined instance's ModelAdmin view """
    template = 'admin/edit_inline/tabular_with_edit.html'


class AddressInline(TabularInlineWithEditLink):
    model = CompanyAddress
    extra = 1
    fields = ['place','address','city','state']


class LocationPhotoInline(admin.TabularInline):
    model = LocationPhoto
    extra = 1


class StartTimeInline(admin.TabularInline):
    model = StartTime
    extra = 1


class CourseInline(TabularInlineWithEditLink):
    model = Course
    extra = 1
    fields = ['title', 'duration', 'audience', 'note']


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


class DealsInlineFormSet(BaseInlineFormSet):
    """ Automatically chooses all a Company's Locations for the Deal.locations value """
    def save_new(self, form, commit=True):
        obj = super(DealsInlineFormSet, self).save_new(form, commit=commit)
        locs = CompanyAddress.objects.filter(company__deal=obj)
        for loc in locs:
            obj.locations.add(loc)
        obj.save()
        return obj


class DealInline(TabularInlineWithEditLink): # admin.TabularInline
    """ 
    Custom inline for Deals on the Company admin.  
     - only works or Company ModelAdmin.
     - overrides widget for TextFields to trim them down
     - excludes several fields
     - by default, saves all the Company's locations as Deal's `locations`

    """
    model = Deal
    extra = 1
    raw_id_fields = ('nonprofit',)
    fields = ['title','price','original_price','fine_print','nonprofit']
    formset = DealsInlineFormSet

    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'cols':30, 'rows':2}),},
    }


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'logo_preview', 'is_partner','enable_products','enable_reviews','enable_courses','enable_pricing']
    list_filter = ['is_partner','enable_products','enable_reviews','enable_courses']
    # fieldsets = (
    #     (None, {'fields': ('name','description','website','logo','is_partner')}),
    # )
    inlines = [AddressInline, DealInline]
    logo_preview = ImgPreview(lambda x: x.logo, ("200x100"))
    search_fields = ['name']
    
    Media = MarkitUpMedia

    def get_urls(self):
        urls = super(CompanyAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'addressajaxlist/$',
                self.admin_site.admin_view(admin_views.company_addressajaxlist),
                name="companies_company_addressajaxlist"
            )
        )
        return my_urls + urls


class CompanyAddressAdmin(admin.ModelAdmin):
    inlines = [CourseInline, ProductInline, LocationPhotoInline]
    list_display = ['place','featured','company','city','has_point']
    list_filter = ['featured']
    exclude = ['point']
    filter_horizontal = ['subcategories']
    raw_id_fields = ['company']
    search_fields = ['place','company__name']
    form = CompanyAdminForm
    prepopulated_fields = {"slug": ("place",)}

    def has_point(self, obj):
        if obj.point:
            return True
        return False
    has_point.boolean = True


class NonProfitAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo', 'website', 'sort_order', 'featured']
    list_editable = ['sort_order',]
    list_filter = ['featured',]
    form = NonProfitForm
    Media = MarkitUpMedia


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name','featured_location']


class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name','category']
    list_filter = ['category']
    search_fields = ['name']


class CourseAdmin(admin.ModelAdmin):
    inlines = [StartTimeInline]
    list_display = ['title','location']
    search_fields = ['title','location__place']


admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyAddress, CompanyAddressAdmin)
admin.site.register(NonProfit, NonProfitAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Course, CourseAdmin)

