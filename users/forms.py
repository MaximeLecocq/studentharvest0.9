from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'address']


class StudentProfileForm(ProfileForm):
    class Meta(ProfileForm.Meta):
        fields = ProfileForm.Meta.fields + ['student_card']


class DonorProfileForm(ProfileForm):
    class Meta(ProfileForm.Meta):
        pass
