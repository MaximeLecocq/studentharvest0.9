from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_backends, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from .forms import DonorProfileForm, StudentProfileForm, ProfileForm, RegistrationForm, CustomLoginForm
from .models import User
from listings.models import Listing


User = get_user_model()

#handles user registration for both students and donors.
#redirects users to complete their profile based on their role (student or donor) after registration.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            #automatically log in the user after registration
            login(request, user, backend='users.authentication_backends.EmailOrUsernameBackend')

            #redirect to profile completion page based on user role
            if user.role == 'student':
                return redirect('complete_profile_student')
            elif user.role == 'donor':
                return redirect('complete_profile_donor')
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})


#allows a student user to complete their profile.
#marks the profile as complete when all required fields are filled.
@login_required
def complete_profile_student(request):
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            #check if the required fields are filled to mark profile as complete
            if (user.first_name and user.last_name and user.phone_number and 
                user.street_address and user.city_town and user.student_card):
                user.complete_profile_student = True

            user.save()  #save the updated user data
            return redirect('profile')  #redirect to user's profile page
    else:
        form = StudentProfileForm(instance=request.user)
    return render(request, 'users/complete_profile_student.html', {'form': form})


#allows a donor user to complete their profile.
@login_required
def complete_profile_donor(request):
    if request.method == 'POST':
        form = DonorProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') #redirect to the profile page after saving
    else:
        form = DonorProfileForm(instance=request.user)
    return render(request, 'users/complete_profile_donor.html', {'form': form})


#handles viewing and editing a user's profile.
@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save() #save profile updates
            return redirect('profile') #reload profile page
    
    else:
        form = ProfileForm(instance=user)
    return render(request, 'users/profile.html', {'form': form})


#logs the user out and redirects them to the homepage.
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect(reverse('homepage'))


#displays a donor's profile and their associated listings.
def donor_profile(request, donor_id):
    donor = get_object_or_404(User, id=donor_id)
    listings = Listing.objects.filter(donor=donor) #get all listings by the donor
    return render(request, 'users/donor_profile.html', {'donor': donor, 'listings': listings})


#custom login view that uses the custom login form.
class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'users/login.html'


#simulated password reset functionality.
def password_reset_done(request):
    return HttpResponse("Password reset link sent (simulated). Check the terminal for instructions.")

#handles the process of confirming a password reset request using a token.
def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            return HttpResponse("Password reset successful (simulated). You can now log in with your new password.")
        else:
            return HttpResponse("Invalid or expired token.")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse("Invalid reset link.")


#renders a page to confirm account deletion.
@login_required
def delete_account_confirm(request):
    return render(request, 'users/confirm_delete.html')


#deletes the user's account and logs them out.
@login_required
def delete_account(request):
    user = request.user
    user.delete()  #this will delete the user's account
    messages.success(request, "Your account has been deleted successfully.")
    return redirect('homepage')