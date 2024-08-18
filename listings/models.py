from django.db import models
from users.models import User
from django.conf import settings


class Listing(models.Model):
    CATEGORY_CHOICES = (
        ('canned', 'Canned Goods'),
        ('dry', 'Dry Staples'),
        ('beverages', 'Beverages'),
        ('vegetables', 'Fresh Vegetables'),
        ('fruits', 'Fruits'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    donor = models.ForeignKey('users.User', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.CharField(max_length=255)  # Comma-separated string of categories
    expiry_date_canned = models.DateField(blank=True, null=True)  # For Canned Goods
    expiry_date_dry = models.DateField(blank=True, null=True)     # For Dry Staples
    expiry_date_beverages = models.DateField(blank=True, null=True)  # For Beverages
    image = models.ImageField(upload_to='images/listings/', blank=True, null=True)
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_listings', blank=True)

    def __str__(self):
        return self.title