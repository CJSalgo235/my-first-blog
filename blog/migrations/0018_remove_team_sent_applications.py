# Generated by Django 2.0.13 on 2019-06-27 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20190627_1713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='sent_applications',
        ),
    ]