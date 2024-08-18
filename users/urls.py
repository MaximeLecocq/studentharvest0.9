from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('profile/student/', views.complete_profile_student, name = 'complete_profile_student'),
    path('profile/donor/', views.complete_profile_donor, name = 'complete_profile_donor'),
    path('profile/', views.profile, name = 'profile'),
    # path('logout/', views.logout_view, name='logout'),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
]