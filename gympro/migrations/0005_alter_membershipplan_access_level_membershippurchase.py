# Generated by Django 5.1.4 on 2024-12-29 12:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gympro', '0004_alter_membershipplan_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membershipplan',
            name='access_level',
            field=models.CharField(choices=[('paprastas', 'Paprastas'), ('premium', 'Premium'), ('auksinis', 'Auksinis'), ('platinum', 'Platinum')], max_length=50),
        ),
        migrations.CreateModel(
            name='MembershipPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(help_text='Narystės galiojimo pabaiga')),
                ('active', models.BooleanField(default=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='gympro.member')),
                ('membership_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gympro.membershipplan')),
            ],
            options={
                'verbose_name': 'Narystės pirkimas',
                'verbose_name_plural': 'Narystės pirkimai',
            },
        ),
    ]
