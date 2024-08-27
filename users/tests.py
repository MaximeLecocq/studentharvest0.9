from django.test import TestCase
from users.forms import RegistrationForm

class RegistrationFormTests(TestCase):
    #test case for invalid form submission due to mismatched passwords.
    #it checks if the form validation catches the mismatch between 'password1' and 'password2'.
    def test_invalid_form_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'minnie', #first password entry
            'password2': 'paul', #second password entry that doesn't match 'password1'
            'role': 'student',
        }
        form = RegistrationForm(data=form_data)
        
        if not form.is_valid():
            print("Form Errors:", form.errors)
        
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    #test case for invalid form submission due to a missing field.
    #it checks if the form validation catches the missing 'password2' field.
    def test_invalid_form_missing_field(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'jean',
            'password2': '',  #missing confirmation password (empty string)
            'role': 'student',
        }
        form = RegistrationForm(data=form_data)
        
        if not form.is_valid():
            print("Form Errors:", form.errors)

        #assert that the form is invalid due to the missing confirmation password.
        self.assertFalse(form.is_valid())
        #assert that the 'password2' field has an error due to being missing.
        self.assertIn('password2', form.errors)