from django.contrib import admin

from .models import Ring


@admin.register(Ring)
class RingAdmin(admin.ModelAdmin):
    """How rings are listed in the Django admin."""

    list_display = ("name", "owner", "style", "metal", "price", "created_on")
    list_filter = ("style", "metal", "gemstone")
    search_fields = ("name", "description", "owner__username")
