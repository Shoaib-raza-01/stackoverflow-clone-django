# Generated by Django 4.2.7 on 2023-12-04 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0011_alter_answer_options_alter_answer_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='answer',
            name='flag',
            field=models.BooleanField(default=True),
        ),
    ]
