# Generated by Django 5.1.4 on 2024-12-25 12:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('specialization', models.CharField(max_length=100)),
                ('bio', models.TextField(blank=True)),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'verbose_name': 'Instruktorius/Treneris',
                'verbose_name_plural': 'Instruktoriai/Treneriai',
                'ordering': ['specialization'],
            },
        ),
        migrations.CreateModel(
            name='MembershipPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(help_text='Plano aprašymas', max_length=200, verbose_name='Aprašymas')),
                ('monthly_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('access_level', models.CharField(choices=[('premium', 'Premium'), ('auksinis', 'Auksinis'), ('platinum', 'Platinum')], max_length=50)),
                ('duration', models.IntegerField(help_text='Trukmė mėnesiais')),
            ],
            options={
                'verbose_name': 'Planas',
                'verbose_name_plural': 'Planai',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SportHall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('hall_type', models.CharField(choices=[('judo', 'Judo'), ('boxo', 'Boxo'), ('treniruokliu', 'Treniruokliu'), ('universali', 'Universali')], max_length=50)),
                ('capacity', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Sporto salė',
                'verbose_name_plural': 'Sporto salės',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('class_type', models.CharField(choices=[('dziudo', 'Dziudo'), ('jiu-jitsu', 'Jiu-jitsu'), ('karate', 'Karate'), ('boksas', 'Boksas'), ('thai-boksas', 'Thai-Boksas'), ('crossfit', 'CrossFit'), ('pilates', 'Pilates'), ('yoga', 'Yoga'), ('zumba', 'Zumba'), ('fitness', 'Fitness')], max_length=50)),
                ('schedule', models.DateTimeField(help_text='Įveskite pamokos datą ir laiką.')),
                ('max_capacity', models.IntegerField()),
                ('current_bookings', models.IntegerField(default=0)),
                ('instructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gympro.instructor')),
                ('sport_hall', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gympro.sporthall')),
            ],
            options={
                'verbose_name': 'Treniruotė',
                'verbose_name_plural': 'Treniruotės',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('join_date', models.DateField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('membership_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gympro.membershipplan')),
            ],
            options={
                'verbose_name': 'Narys',
                'verbose_name_plural': 'Nariai',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('class_session', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gympro.class')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gympro.member')),
            ],
            options={
                'verbose_name': 'Registracija',
                'verbose_name_plural': 'Registracijos',
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('equipment_type', models.CharField(choices=[('cardio', 'Cardio'), ('strength', 'Strength'), ('free weights', 'Free Weights')], max_length=50)),
                ('purchase_date', models.DateField()),
                ('condition', models.CharField(choices=[('naujas', 'Naujas'), ('geras', 'Geras'), ('reikalauja aptarnavimo', 'Reikalauja aptarnavimo')], max_length=30)),
                ('sport_hall', models.ForeignKey(limit_choices_to={'hall_type': 'treniruokliu'}, on_delete=django.db.models.deletion.CASCADE, to='gympro.sporthall')),
            ],
            options={
                'verbose_name': 'Treniruoklis',
                'verbose_name_plural': 'Treniruokliai',
            },
        ),
    ]