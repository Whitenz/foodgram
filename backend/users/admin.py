from django.contrib import admin
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import TokenProxy

from .models import CustomTokenProxy, Subscription

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'first_name',
                    'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    list_editable = ('username', 'email', 'first_name', 'last_name')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_from', 'user_to')
    list_filter = ('user_from', 'user_to')
    list_editable = ('user_from', 'user_to')


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(CustomTokenProxy)
admin.site.unregister(TokenProxy)
