# Generated by Django 5.1.4 on 2025-01-02 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gympro', '0007_remove_membershippurchase_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classes', to='gympro.instructor'),
        ),
    ]