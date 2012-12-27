import csv
from cStringIO import StringIO

from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.template.defaultfilters import date as date_filter

from models import Widget

class WidgetAdmin(admin.ModelAdmin):
    list_display = ['title', 'api_key', 'widget_munged_html', 'view_count', 'order_count', 'preview_link', 'export_link']
    fieldsets = (
        (None, {
            'fields': ('title', 'api_key')
        }),
        ('Styles', {
            'fields': ('link_color', 'link_hover_color', 'bg_image', 'nav_image')
        }),
    )
    
    def export_link(self, obj):
        widget = Widget.objects.get(id=obj.id)
        if widget.orders.count() > 0:
            return u'<a href="./export/%s/">export</a>' % obj.id
        else:
            return ''
    export_link.allow_tags = True
    
    def preview_link(self, obj):
        return '<a href="./preview/%s/" target="_blank">preview</a>' % obj.id
    preview_link.allow_tags = True
    
    def get_urls(self):
        urls = super(WidgetAdmin, self).get_urls()
        widget_urls = patterns('',
            url(r'export/(\d+)/$',
                self.admin_site.admin_view(self.export_csv), name="export_widget"
            ),
            url(r'preview/(\d+)/$',
                self.admin_site.admin_view(self.preview_widget), name="preview_widget"
            )
        )
        return widget_urls + urls
        
    # Admin views for preview and export
    def preview_widget(self, request, widget_id):
        widget = Widget.objects.get(id=widget_id)
        return render_to_response('widget/widget-test.html', {'widget': widget}, RequestContext(request))
    
    def export_csv(self, request, widget_id):
        stream = StringIO()
        writer = csv.writer(stream)
        writer.writerow(['Firstname', 'Lastname', 'Email', 'Deal', 'Selected Non-Profit', 'Purchase Date', 'Purchase Time'])
        widget = Widget.objects.get(id=widget_id)
        for order in widget.orders.all():
            for i in order.deals.all():
                writer.writerow([
                    order.account.first_name,           # Firstname
                    order.account.last_name,            # lastname
                    order.account.email,                # email address
                    i.deal.title,
                    str(i.nonprofit),               # Selected Non-Profit
                    date_filter(order.date, 'm/d/y'),
                    date_filter(order.date, 'P'),
                ])
        response = HttpResponse(stream.getvalue(), 'text/csv')
        response['Content-Disposition'] = 'attachment; filename=widget.csv'
        return response

admin.site.register(Widget, WidgetAdmin)
