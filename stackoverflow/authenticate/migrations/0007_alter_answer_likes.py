# Generated by Django 4.2.7 on 2023-12-01 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0006_question_views_question_votes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='Likes',
            field=models.IntegerField(default=0),
        ),
    ]