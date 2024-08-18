# listings/forms.py

from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    CATEGORIES = (
        ('canned', 'Canned Goods'),
        ('dry', 'Dry Staples'),
        ('beverages', 'Beverages'),
        ('vegetables', 'Fresh Vegetables'),
        ('fruits', 'Fruits'),
    )
    
    categories = forms.MultipleChoiceField(
        choices=CATEGORIES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    # Fields for expiry dates
    expiry_date_canned = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    expiry_date_dry = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    expiry_date_beverages = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Listing
        fields = ['title', 'description', 'address', 'categories', 'expiry_date_canned', 'expiry_date_dry', 'expiry_date_beverages', 'image']

    def clean(self):
        cleaned_data = super().clean()
        categories = cleaned_data.get('categories')
        
        # Ensure expiry dates for certain categories are filled
        if 'canned' in categories and not cleaned_data.get('expiry_date_canned'):
            self.add_error('expiry_date_canned', 'Expiry date is required for Canned Goods.')
        if 'dry' in categories and not cleaned_data.get('expiry_date_dry'):
            self.add_error('expiry_date_dry', 'Expiry date is required for Dry Staples.')
        if 'beverages' in categories and not cleaned_data.get('expiry_date_beverages'):
            self.add_error('expiry_date_beverages', 'Expiry date is required for Beverages.')

        return cleaned_data
