from django.contrib import admin
from .models import Listing

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'donor', 'created_at', 'expiry_date_canned', 'expiry_date_dry', 'expiry_date_beverages')
    list_filter = ('created_at', 'expiry_date_canned', 'expiry_date_dry', 'expiry_date_beverages')
    search_fields = ('title', 'description', 'donor__username')

admin.site.register(Listing, ListingAdmin)

