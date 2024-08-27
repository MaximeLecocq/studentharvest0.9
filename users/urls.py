from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('profile/student/', views.complete_profile_student, name = 'complete_profile_student'),
    path('profile/donor/', views.complete_profile_donor, name = 'complete_profile_donor'),
    path('profile/', views.profile, name = 'profile'),
    path('donor/<int:donor_id>/', views.donor_profile, name='donor_profile'),

    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),


    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('profile/delete/confirm/', views.delete_account_confirm, name='delete_account_confirm'),
    path('profile/delete/', views.delete_account, name='delete_account'),
]