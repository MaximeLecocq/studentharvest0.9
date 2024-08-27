from django.test import TestCase
from listings.models import Listing
from users.models import User
from datetime import date
from listings.forms import ListingForm

class ListingModelTest(TestCase):
    def setUp(self):
        #set up a user (donor) for use in the tests
        self.donor = User.objects.create_user(username='donor', password='testpass')

    def test_listing_creation(self):
        #test that a listing can be created and its string representation is correct
        listing = Listing.objects.create(
            title='Canned Beans',
            description='Fresh canned beans',
            donor=self.donor,
            street_address='123 Street',
            city='Test City',
            categories='canned',
            expiry_date_canned=date.today(),
            image1='image1.jpg'
        )
        #check that the string representation of the listing matches the title
        self.assertEqual(str(listing), 'Canned Beans')

    def test_expiry_date(self):
        #test that a canned listing has an expiry date
        listing = Listing.objects.create(
            title='Canned Beans',
            description='Fresh canned beans',
            donor=self.donor,
            categories='canned',
            expiry_date_canned=date.today(),
            image1='image1.jpg'
        )
        #assert that the expiry date is not None
        self.assertIsNotNone(listing.expiry_date_canned)


class ListingFormTest(TestCase):
    def test_missing_expiry_date(self):
        #test that the form is invalid if an expiry date is missing for a canned category
        form_data = {
            'title': 'Test Title',
            'description': 'Test Description',
            'street_address': '123 Test St',
            'city': 'Test City',
            'categories': ['canned'], #category requiring an expiry date
        }
        form_files = {'image1': 'test_image.jpg'}
        form = ListingForm(data=form_data, files=form_files)
        #assert that the form is not valid because the expiry date is missing
        self.assertFalse(form.is_valid())
        #assert that the error message relates to the missing expiry date for canned goods
        self.assertIn('expiry_date_canned', form.errors)

    def test_missing_image(self):
        #test that the form is invalid if the mandatory image1 is missing
        form_data = {
            'title': 'Test Title',
            'description': 'Test Description',
            'street_address': '123 Test St',
            'city': 'Test City',
            'categories': ['canned'], #valid category
            'expiry_date_canned': date.today(), #valid expiry date
        }
        #creating the form without an image
        form = ListingForm(data=form_data)
        #assert that the form is not valid because image1 is missing
        self.assertFalse(form.is_valid())
        #assert that the error message relates to the missing image1 field
        self.assertIn('image1', form.errors)