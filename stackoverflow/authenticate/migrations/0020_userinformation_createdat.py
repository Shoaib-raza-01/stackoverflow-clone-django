# Generated by Django 4.2.7 on 2023-12-07 05:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0019_userinformation_bookmarked'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='CreatedAt',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]