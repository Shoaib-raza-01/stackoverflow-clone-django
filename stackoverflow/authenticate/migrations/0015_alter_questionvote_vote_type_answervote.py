# Generated by Django 4.2.7 on 2023-12-04 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authenticate', '0014_questionvote_vote_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionvote',
            name='vote_type',
            field=models.CharField(max_length=4),
        ),
        migrations.CreateModel(
            name='AnswerVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.CharField(max_length=4)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authenticate.answer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'answer')},
            },
        ),
    ]