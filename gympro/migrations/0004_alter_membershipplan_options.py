# Generated by Django 5.1.4 on 2024-12-29 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gympro', '0003_sporthall_photo_alter_sporthall_hall_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membershipplan',
            options={'ordering': ['name'], 'verbose_name': 'Narystė', 'verbose_name_plural': 'Narystės'},
        ),
    ]