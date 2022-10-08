from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from .models import CustomTokenProxy, Subscription
from recipes.models import Cart, Favorite

User = get_user_model()


class CartInline(admin.TabularInline):
    model = Cart
    extra = 0


class FavoriteInline(admin.StackedInline):
    model = Favorite
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'first_name',
                    'last_name', 'is_staff')
    exclude = ('groups',)
    readonly_fields = ('date_joined', 'last_login')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    list_editable = ('username', 'email', 'first_name', 'last_name')
    inlines = (CartInline, FavoriteInline)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_from', 'user_to')
    list_filter = ('user_from', 'user_to')
    list_editable = ('user_from', 'user_to')


@admin.register(CustomTokenProxy)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    readonly_fields = ('user',)


admin.site.unregister(TokenProxy)
admin.site.unregister(Group)
