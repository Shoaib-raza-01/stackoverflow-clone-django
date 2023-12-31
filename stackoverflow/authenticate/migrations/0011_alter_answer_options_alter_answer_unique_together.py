# Generated by Django 4.2.7 on 2023-12-04 05:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authenticate', '0010_remove_comment_likes_alter_comment_answer_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-CreatedAt']},
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together={('Likes', 'user', 'Content')},
        ),
    ]
