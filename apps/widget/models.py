import string
import random
from datetime import datetime

from django.db import models
from django.contrib.sites.models import Site
from django.utils.html import escape
from django.utils.safestring import mark_safe

from activebuys.apps.accounts.models import Order

def random_string():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(25))

class Widget(models.Model):
    title = models.CharField(max_length=250)
    api_key = models.CharField(max_length=25, default=random_string(), unique=True)
    link_color = models.CharField(max_length=7, default="#6A8C0F", help_text="Hex value for link color.")
    link_hover_color = models.CharField(max_length=7, default="#383838", help_text="Hex value for link color on hover.")
    bg_image = models.ImageField(blank=True, upload_to='uploads/widgets/')
    nav_image = models.ImageField(blank=True, upload_to='uploads/widgets/')
    orders = models.ManyToManyField(Order, blank=True)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title
        
    def widget_munged_html(self):
        # Munge the code into plain ASCII for proper display
        # Courtesy of http://www.addressmunger.com/display_code/
        html = '&#60;&#33;&#45;&#45;&#32;&#83;&#116;&#97;&#114;&#116;&#32;&#65;&#67;&#84;&#73;&#86;&#69;&#66;&#85;&#89;&#83;&#32;&#87;&#105;&#100;&#103;&#101;&#116;&#32;&#45;&#45;&#62;<br />\
                &#60;&#115;&#99;&#114;&#105;&#112;&#116;&#32;&#116;&#121;&#112;&#101;&#61;&#34;&#116;&#101;&#120;&#116;&#47;&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#34;&#62;<br />\
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;var _abwparam = _abwparam || [];<br />\
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_abwparam["APIKEY"] = "%s";<br />\
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_abwparam["link_color"] = "%s";<br />\
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_abwparam["hover_color"] = "%s";<br />\
                &#60;&#47;&#115;&#99;&#114;&#105;&#112;&#116;&#62;<br />\
                &#60;&#115;&#99;&#114;&#105;&#112;&#116;&#32;&#116;&#121;&#112;&#101;&#61;&#34;&#116;&#101;&#120;&#116;&#47;&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#34;&#32;&#115;&#114;&#99;&#61;&#34;http://%s/static/widget/widget.js&#34;&#62;&#60;&#47;&#115;&#99;&#114;&#105;&#112;&#116;&#62;<br />\
                &#60;&#97;&#32;&#105;&#100;&#61;&#34;&#97;&#99;&#116;&#105;&#118;&#101;&#45;&#98;&#117;&#121;&#115;&#45;&#119;&#105;&#100;&#103;&#101;&#116;&#34;&#32;&#104;&#114;&#101;&#102;&#61;&#34;&#104;&#116;&#116;&#112;&#58;&#47;&#47;&#97;&#99;&#116;&#105;&#118;&#101;&#98;&#117;&#121;&#115;&#46;&#99;&#111;&#109;&#47;&#34;&#62;&#86;&#105;&#115;&#105;&#116;&#32;&#65;&#67;&#84;&#73;&#86;&#69;&#66;&#85;&#89;&#83;&#32;&#70;&#111;&#114;&#32;&#68;&#97;&#105;&#108;&#121;&#32;&#68;&#101;&#97;&#108;&#115;&#60;&#47;&#97;&#62;<br />\
                &#60;&#33;&#45;&#45;&#32;&#69;&#110;&#100;&#32;&#65;&#67;&#84;&#73;&#86;&#69;&#66;&#85;&#89;&#83;&#32;&#87;&#105;&#100;&#103;&#101;&#116;&#32;&#45;&#45;&#62;' % (self.api_key, self.link_color, self.link_hover_color, Site.objects.get_current().domain)
        return html
    widget_munged_html.short_description = 'HTML'
    widget_munged_html.allow_tags = True
        
    def widget_html(self):
        html = '<!-- Start ACTIVEBUYS Widget -->\
            	<script type="text/javascript">\
                    var _abwparam = _abwparam || [];\
                    _abwparam["APIKEY"] = "%s";\
                    _abwparam["link_color"] = "%s";\
                    _abwparam["hover_color"] = "%s";\
                </script>\
            	<script type="text/javascript" src="http://%s/static/widget/widget.js"></script>\
            	<a id="active-buys-widget" href="http://activebuys.com/">Visit ACTIVEBUYS For Daily Deals</a>\
            	<!-- End ACTIVEBUYS Widget -->' % (self.api_key, self.link_color, self.link_hover_color, Site.objects.get_current().domain)
        return html
    
    def order_count(self):
        return self.orders.count()