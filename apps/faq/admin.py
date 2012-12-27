from django.contrib import admin
from models import FAQ


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question']
    
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


admin.site.register(FAQ, FAQAdmin)