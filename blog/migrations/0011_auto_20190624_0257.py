# Generated by Django 2.0.13 on 2019-06-24 02:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_team_sent_applications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='sent_applications',
            field=models.ManyToManyField(blank=True, related_name='sent_applications', to=settings.AUTH_USER_MODEL),
        ),
    ]
