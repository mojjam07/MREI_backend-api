from django.contrib import admin
from .models import Announcement, Notification, ContactMessage


# Register your models here.
admin.site.register(Announcement)
admin.site.register(Notification)
admin.site.register(ContactMessage)
