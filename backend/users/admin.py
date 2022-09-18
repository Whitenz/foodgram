from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Subscription

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'first_name',
                    'last_name', 'is_staff')
    list_filter = ('username', 'email')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_from', 'user_to')
    list_filter = ('user_from', 'user_to')


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
