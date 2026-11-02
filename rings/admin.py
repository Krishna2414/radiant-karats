from django.contrib import admin

from .models import Favourite, Ring


@admin.register(Ring)
class RingAdmin(admin.ModelAdmin):
    """How rings are listed in the Django admin."""

    list_display = ("name", "owner", "style", "metal", "price", "created_on")
    list_filter = ("style", "metal", "gemstone")
    search_fields = ("name", "description", "owner__username")


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    """Which users have saved which rings to their Favourites."""

    list_display = ("ring", "user", "created_on")
    search_fields = ("ring__name", "user__username")
