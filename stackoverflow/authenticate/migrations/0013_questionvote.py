# Generated by Django 4.2.7 on 2023-12-04 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authenticate', '0012_alter_answer_unique_together_answer_flag'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authenticate.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'question')},
            },
        ),
    ]
