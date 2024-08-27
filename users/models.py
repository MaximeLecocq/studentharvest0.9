from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    #choose role choice
    USER_ROLE_CHOICES = (
        ('student', 'Student'),
        ('donor', 'Donor'),
    )

    #fields for all users
    role = models.CharField('User Role', max_length=10, choices=USER_ROLE_CHOICES, default='student')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    street_address = models.CharField('Street Number and Name', max_length=255, blank=True, null=True)
    city_town = models.CharField('City/Town', max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='images/avatars/', blank=True, null=True)
    complete_profile_student = models.BooleanField(default=False)
    about = models.TextField('About', blank=True, null=True)

    #extra field for students
    student_card = models.ImageField(upload_to='student_cards/', blank=True, null=True)

    def __str__(self):
        return self.username
