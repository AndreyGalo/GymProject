# Generated by Django 5.1.4 on 2024-12-26 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gympro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='instructors_photos/'),
        ),
    ]