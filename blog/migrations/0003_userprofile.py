# Generated by Django 2.0.13 on 2019-06-22 09:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=100)),
                ('city', models.CharField(default='', max_length=50)),
                ('website', models.URLField(default='', max_length=100)),
                ('phone', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
