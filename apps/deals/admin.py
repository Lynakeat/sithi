import csv
from cStringIO import StringIO
from datetime import datetime

from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from django.http import HttpResponse
from django.template.defaultfilters import date as date_filter

from activebuys.apps.utils.admin import ImgPreview
from models import Deal, Picture, Background
from activebuys.apps.accounts.models import AccountDeal, Order
#from django.core.urlresolvers import reverse


class PictureInline(admin.TabularInline):
    model = Picture


class DealAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'price', 'original_price',
        'sold', 'company',
        'start_time', 'end_time', 'featured',
        'past_featured', 'home_page', 'active',
        'export_link'
    ]
    list_filter = ['featured', 'past_featured', 'home_page']
    raw_id_fields = ('company', 'background')
    inlines = [PictureInline]
    prepopulated_fields = {'slug': ('title',),} # not working: 'original_price': ('price',)
    search_fields = ['title', 'company__name']

    def active(self, obj):
        return obj.start_time <= datetime.now() and obj.end_time > datetime.now()
    active.boolean = True

    def export_link(self, obj):
        return u'<a href="./export/%s/">export</a>' % obj.id
    export_link.allow_tags = True

    def get_urls(self):
        urls = super(DealAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'export/(\d+)/$',
                self.admin_site.admin_view(self.export_csv), name="export_deals"
            )
        )
        return my_urls + urls

    def export_csv(self, request, deal_id):
        stream = StringIO()
        writer = csv.writer(stream)
        writer.writerow(['Voucher', 'Firstname', 'Lastname', 'Email', 'Gift Recipient', 'Company', 'Selected Location', 'Selected Non-Profit', 'Purchase Date', 'Purchase Time'])
        for i in AccountDeal.objects.active().filter(deal__id=deal_id):
            order = Order.objects.get(deals=i, account=i.account)

            writer.writerow([
                i.voucher.code,                 # Voucher Code
                i.account.first_name,           # Firstname
                i.account.last_name,            # lastname
                i.account.email,                # email address
                i.is_gift and i.name_to or ' ', # Gift Recipient Name, if applicable
                i.deal.company.name,            # Company Name
                str(i.location),                # Selected Location
                str(i.nonprofit),               # Selected Non-Profit
                date_filter(order.date, 'm/d/y'),
                date_filter(order.date, 'P'),
            ])
        response = HttpResponse(stream.getvalue(), 'text/csv')
        response['Content-Disposition'] = 'attachment; filename=deals.csv'
        return response

    class Media:
        js = (
            'js/jquery-1.6.1.min.js',
            'js/markitup/jquery.markitup.pack.js',
            'js/markitup/sets/markdown/set.js',
            'js/markitup_admin.js',
            'js/admin_populate_locations.js'
        )
        css = {
            'all': (
                'js/markitup/skins/simple/style.css',
                'js/markitup/sets/markdown/style.css',
            )
        }


class BackgroundAdmin(admin.ModelAdmin):
    list_display = ['title', 'preview']
    preview = ImgPreview(lambda x: x.image, ("200x100"))


admin.site.register(Deal, DealAdmin)
admin.site.register(Background, BackgroundAdmin)
