# Generated by Django 5.1.4 on 2024-12-29 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gympro', '0002_instructor_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='sporthall',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='sporto_sales_photos/'),
        ),
        migrations.AlterField(
            model_name='sporthall',
            name='hall_type',
            field=models.CharField(choices=[('judo', 'Judo'), ('boxing', 'Boxing'), ('treniruokliu', 'Treniruokliu'), ('universali', 'Universali')], max_length=50),
        ),
    ]
