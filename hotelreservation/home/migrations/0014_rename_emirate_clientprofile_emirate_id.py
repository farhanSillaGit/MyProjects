# Generated by Django 4.2.7 on 2023-11-19 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_rename_emirates_clientprofile_emirate_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientprofile',
            old_name='emirate',
            new_name='emirate_id',
        ),
    ]
