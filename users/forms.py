from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
        
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'peer block w-full rounded border-0 bg-transparent px-3 py-[0.32rem] leading-[2.15] outline-none focus:text-primary placeholder-opacity-0 transition duration-200 ease-linear',
        'placeholder': 'Username'
    }))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'peer block w-full rounded border-0 bg-transparent px-3 py-[0.32rem] leading-[2.15] outline-none focus:text-primary placeholder-opacity-0 transition duration-200 ease-linear',
        'placeholder': 'Email address'
    }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'peer block w-full rounded border-0 bg-transparent px-3 py-[0.32rem] leading-[2.15] outline-none focus:text-primary placeholder-opacity-0 transition duration-200 ease-linear',
        'placeholder': 'Password'
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'peer block w-full rounded border-0 bg-transparent px-3 py-[0.32rem] leading-[2.15] outline-none focus:text-primary placeholder-opacity-0 transition duration-200 ease-linear',
        'placeholder': 'Confirm Password'
    }))
    
    role = forms.ChoiceField(choices=User.USER_ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'peer block w-full rounded border-0 bg-transparent px-3 py-[0.32rem] leading-[2.15] outline-none focus:text-primary placeholder-opacity-0 transition duration-200 ease-linear',
    }))



#profile form for donors and other users
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'street_address', 'city_town', 'about', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'First Name',
                'style': 'border: 1px solid #d1d5db; border-radius: 0.375rem; padding: 0.5rem 0.75rem; width: 100%;'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Last Name',
                'style': 'border: 1px solid #d1d5db; border-radius: 0.375rem; padding: 0.5rem 0.75rem; width: 100%;'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Phone Number',
                'style': 'border: 1px solid #d1d5db; border-radius: 0.375rem; padding: 0.5rem 0.75rem; width: 100%;'
            }),
            'street_address': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Street Address',
                'style': 'border: 1px solid #d1d5db; border-radius: 0.375rem; padding: 0.5rem 0.75rem; width: 100%;'
            }),
            'city_town': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'City/Town',
                'style': 'border: 1px solid #d1d5db; border-radius: 0.375rem; padding: 0.5rem 0.75rem; width: 100%;'
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Write a brief introduction about yourself...',
                'style': 'border: 1px solid #d1d5db; border-radius: 0.375rem; padding: 0.5rem 0.75rem; width: 100%;',
                'rows': 4,
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-input',
                'style': 'border: 1px solid #d1d5db; border-radius: 0.375rem; padding: 0.5rem 0.75rem; width: 100%;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #ensure fields are marked as required by default
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['phone_number'].required = True
        self.fields['street_address'].required = True
        self.fields['city_town'].required = True


#profile Form specifically for students
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'street_address', 'city_town', 'about','student_card', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'First Name',
                'style': 'border: 1px solid #d1d5db; border-radius: 0.375rem; padding: 0.5rem 0.75rem; width: 100%;'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Last Name',
                'style': 'border: 1px solid #d1d5db; border-radius: 0.375rem; padding: 0.5rem 0.75rem; width: 100%;'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Phone Number',
                'style': 'border: 1px solid #d1d5db; border-radius: 0.375rem; padding: 0.5rem 0.75rem; width: 100%;'
            }),
            'street_address': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Street Address',
                'style': 'border: 1px solid #d1d5db; border-radius: 0.375rem; padding: 0.5rem 0.75rem; width: 100%;'
            }),
            'city_town': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'City/Town',
                'style': 'border: 1px solid #d1d5db; border-radius: 0.375rem; padding: 0.5rem 0.75rem; width: 100%;'
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Write a brief introduction about yourself...',
                'style': 'border: 1px solid #d1d5db; border-radius: 0.375rem; padding: 0.5rem 0.75rem; width: 100%;',
                'rows': 4,
            }),
            'student_card': forms.ClearableFileInput(attrs={
                'class': 'form-input',
                'style': 'border: 1px solid #d1d5db; border-radius: 0.375rem; padding: 0.5rem 0.75rem; width: 100%;'
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-input',
                'style': 'border: 1px solid #d1d5db; border-radius: 0.375rem; padding: 0.5rem 0.75rem; width: 100%;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #ensure fields are marked as required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['phone_number'].required = True
        self.fields['street_address'].required = True
        self.fields['city_town'].required = True
        self.fields['student_card'].required = True

class DonorProfileForm(ProfileForm):
    class Meta(ProfileForm.Meta):
        pass


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
            'placeholder': 'Username or Email',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
            'placeholder': 'Password',
        })
    )


class CustomPasswordResetForm(PasswordResetForm):
    pass
