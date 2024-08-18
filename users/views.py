from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import DonorProfileForm, StudentProfileForm, ProfileForm, RegistrationForm
from .models import User


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'student':
                return redirect ('complete_profile_student')
            elif user.role == 'donor':
                return redirect('complete_profile_donor')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def complete_profile_student(request):
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = StudentProfileForm(instance=request.user)
    return render(request, 'users/complete_profile_student.html', {'form': form})


@login_required
def complete_profile_donor(request):
    if request.method == 'POST':
        form = DonorProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = DonorProfileForm(instance=request.user)
    return render(request, 'users/complete_profile_donor.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    
    else:
        form = ProfileForm(instance=user)
    return render(request, 'users/profile.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect(reverse('homepage'))