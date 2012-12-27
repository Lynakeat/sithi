from django.contrib import admin
#from django.contrib.auth.models import User, Group

from django.contrib.auth.admin import UserAdmin

from models import Account, AccountDeal, SubscribeLocation, Order
from forms import AdminAccountCreateForm, AdminAccountChangeForm

class AccountAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_superuser', 'is_staff', 'is_active', 'referred_email']
    list_filter = ['subscribe_location', 'is_superuser', 'is_staff', 'is_active']
    fieldsets = (
        (None, {
            'fields': (
                'username', ('first_name', 'last_name'),'email', 'subscribe_location', 'password',
                'is_superuser', 'is_staff', 'is_active',
                'referred_email', 'foxycart_customer_id'
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2')}
        ),
    )
    form = AdminAccountChangeForm
    add_form = AdminAccountCreateForm


class AccountDelaAdmin(admin.ModelAdmin):
    list_display = ['account', 'deal', 'location', 'is_gift', 'surprise', 'timestamp', 'status']
    list_filter = ['is_gift', 'surprise', 'status']
    raw_id_fields = ['account', 'deal', 'nonprofit']
    fieldsets = (
        (None, {
            'fields': ('status', 'account', 'deal', 'location', 'nonprofit', 'widget_id')
        }),
        ('Gift', {
            'fields': ('is_gift', 'name_to', 'name_from', 'message', ('email_to', 'surprise'))
        }),
    )

class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ['deals',]

#admin.site.unregister(User)
#admin.site.unregister(Group)
admin.site.register(Account, AccountAdmin)
admin.site.register(AccountDeal, AccountDelaAdmin)
admin.site.register(SubscribeLocation)
admin.site.register(Order, OrderAdmin)
