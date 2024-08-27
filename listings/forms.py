from django import forms
from .models import Listing
from datetime import date

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
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox shadow-sm'}),
        required=True
    )

    today = date.today().strftime('%Y-%m-%d')


    #fields for expiry dates with 'min' attribute
    expiry_date_canned = forms.DateField(
        required=False, 
        widget=forms.TextInput(attrs={'type': 'date', 'min': today})
    )
    expiry_date_dry = forms.DateField(
        required=False, 
        widget=forms.TextInput(attrs={'type': 'date', 'min': today})
    )
    expiry_date_beverages = forms.DateField(
        required=False, 
        widget=forms.TextInput(attrs={'type': 'date', 'min': today})
    )

    #separate fields for address
    street_address = forms.CharField(
        max_length=255, 
        required=True, 
        label='Street Address',
        widget=forms.TextInput(attrs={'class': 'form-input shadow-md border border-gray-300 rounded-md p-2', 'placeholder': 'Enter street address'})
    )
    city = forms.CharField(
        max_length=100, 
        required=True, 
        label='City/Town',
        widget=forms.TextInput(attrs={'class': 'form-input shadow-md border border-gray-300 rounded-md p-2', 'placeholder': 'Enter city or town'})
    )

    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'street_address', 'city', 'categories',
            'expiry_date_canned', 'expiry_date_dry', 'expiry_date_beverages',
            'image1', 'image2', 'image3'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input shadow-md border border-gray-300 rounded-md p-2 placeholder-gray-500',
                'placeholder': 'Enter the title of the listing'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input shadow-md border border-gray-300 rounded-md p-2',
                'placeholder': 'Enter a detailed description'
            }),
            'image1': forms.ClearableFileInput(attrs={'class': 'form-input shadow-md border border-gray-300 rounded-md p-2'}),
            'image2': forms.ClearableFileInput(attrs={'class': 'form-input shadow-md border border-gray-300 rounded-md p-2'}),
            'image3': forms.ClearableFileInput(attrs={'class': 'form-input shadow-md border border-gray-300 rounded-md p-2'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        categories = cleaned_data.get('categories', [])

        #ensure 'categories' is a list, even if empty
        if not isinstance(categories, list):
            categories = []

        #ensure expiry dates for certain categories are filled
        if 'canned' in categories and not cleaned_data.get('expiry_date_canned'):
            self.add_error('expiry_date_canned', 'Expiry date is required for Canned Goods.')
        if 'dry' in categories and not cleaned_data.get('expiry_date_dry'):
            self.add_error('expiry_date_dry', 'Expiry date is required for Dry Staples.')
        if 'beverages' in categories and not cleaned_data.get('expiry_date_beverages'):
            self.add_error('expiry_date_beverages', 'Expiry date is required for Beverages.')

        return cleaned_data



class SearchForm(forms.Form):
    title = forms.CharField(max_length=100, required=False, label='Search by Title')
    city = forms.CharField(max_length=100, required=False, label='Search by City/Town')
    
    CATEGORY_CHOICES = [
        ('canned', 'Canned Goods'),
        ('dry', 'Dry Staples'),
        ('beverages', 'Beverages'),
        ('vegetables', 'Fresh Vegetables'),
        ('fruits', 'Fruits'),
    ]
    
    categories = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Categories'
    )