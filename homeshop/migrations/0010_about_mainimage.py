# Generated by Django 5.2 on 2025-04-26 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeshop', '0009_about_centre1image_about_centre2image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='about',
            name='mainimage',
            field=models.ImageField(null=True, upload_to='images/centre3'),
        ),
    ]
