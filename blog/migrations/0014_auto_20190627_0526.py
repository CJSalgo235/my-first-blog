# Generated by Django 2.0.13 on 2019-06-27 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20190624_0624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invite',
            name='sent_invite',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]
