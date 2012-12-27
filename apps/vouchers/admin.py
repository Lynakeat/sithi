from django.contrib import admin
from models import Voucher


class VoucherAdmin(admin.ModelAdmin):
    list_display = ['code', 'deal', 'user', 'is_used', 'pdf']

    def deal(self, obj):
        return obj.accountdeal.deal
    deal.short_description = "Deal"
    
    def user(self, obj):
        return obj.accountdeal.account.get_full_name()
    user.short_description = "User"


admin.site.register(Voucher, VoucherAdmin)