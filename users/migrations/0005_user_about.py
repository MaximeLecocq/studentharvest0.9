# Generated by Django 5.0.6 on 2024-08-25 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_complete_profile_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, null=True, verbose_name='About'),
        ),
    ]
