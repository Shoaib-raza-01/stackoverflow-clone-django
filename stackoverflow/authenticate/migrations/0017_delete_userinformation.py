# Generated by Django 4.2.7 on 2023-12-06 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0016_userinformation_bookmarked'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserInformation',
        ),
    ]