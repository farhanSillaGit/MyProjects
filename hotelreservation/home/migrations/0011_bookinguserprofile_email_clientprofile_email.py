# Generated by Django 4.2.7 on 2023-11-17 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_customuser_is_booking_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinguserprofile',
            name='email',
            field=models.EmailField(default=None, max_length=254),
        ),
        migrations.AddField(
            model_name='clientprofile',
            name='email',
            field=models.EmailField(default=None, max_length=254),
        ),
    ]
