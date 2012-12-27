from django.contrib import admin
from activebuys.apps.contacts.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'subject', 'phone']


admin.site.register(Message, MessageAdmin)
