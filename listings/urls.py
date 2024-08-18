from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('create/', views.create_listing, name='create_listing'),
    path('listings/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listings/<int:pk>/edit/', views.edit_listing, name='edit_listing'),
    path('donor/<int:donor_id>/', views.donor_listings, name='donor_listings'),
    path('listings/<int:pk>/delete/', views.delete_listing, name='delete_listing'),
    path('favorites/', views.user_favorites, name='user_favorites'),
    path('listings/<int:pk>/add-to-favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('listings/<int:pk>/remove-from-favorites/', views.remove_from_favorites, name='remove_from_favorites'),
]