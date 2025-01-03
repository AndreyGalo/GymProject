from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class MembershipPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField("Aprašymas", max_length=200, help_text="Plano aprašymas")
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='membership_logos/', blank=True, null=True)
    access_level = models.CharField(
        max_length=50,
        choices=[
            ('paprastas', 'Paprastas'),
            ('premium', 'Premium'),
            ('auksinis', 'Auksinis'),
            ('platinum', 'Platinum')]
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Narystė"
        verbose_name_plural = "Narystės"


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    join_date = models.DateField(auto_now_add=True)
    membership_type = models.ForeignKey("MembershipPlan", on_delete=models.SET_NULL, null=True, default=4)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Narys"
        verbose_name_plural = "Nariai"


class MembershipPurchase(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="purchases")
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(help_text="Narystės galiojimo pabaiga", null=True, blank=True)

    def __str__(self):
        return f"{self.member} - {self.membership_plan.name}"

    class Meta:
        verbose_name = "Narystės pirkimas"
        verbose_name_plural = "Narystės pirkimai"


class SportHall(models.Model):
    name = models.CharField(max_length=30)
    hall_type = models.CharField(max_length=50, choices=[
        ('judo', 'Judo'),
        ('boxing', 'Boxing'),
        ('treniruokliu', 'Treniruokliu'),
        ('universali', 'Universali')
    ])
    capacity = models.IntegerField()
    photo = models.ImageField(upload_to='sporto_sales_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Sporto salė"
        verbose_name_plural = "Sporto salės"


class Instructor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    specialization = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    photo = models.ImageField(upload_to='instructors_photos/', blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["specialization"]
        verbose_name = "Instruktorius/Treneris"
        verbose_name_plural = "Instruktoriai/Treneriai"


class Class(models.Model):
    name = models.CharField(max_length=30)
    class_type = models.CharField(max_length=50, choices=[
        ('dziudo', 'Dziudo'),
        ('jiu-jitsu', 'Jiu-jitsu'),
        ('karate', 'Karate'),
        ('boksas', 'Boksas'),
        ('thai-boksas', 'Thai-Boksas'),
        ('crossfit', 'CrossFit'),
        ('pilates', 'Pilates'),
        ('yoga', 'Yoga'),
        ('zumba', 'Zumba'),
        ('fitness', 'Fitness'),
    ])
    instructor = models.ForeignKey("Instructor", on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="classes")
    sport_hall = models.ForeignKey("SportHall", on_delete=models.SET_NULL, null=True, blank=True)
    schedule = models.DateTimeField(help_text="Įveskite pamokos datą ir laiką.", default=timezone.now)
    max_capacity = models.IntegerField()
    current_bookings = models.IntegerField(default=0)

    @property
    def is_full(self):
        return self.current_bookings >= self.max_capacity

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Treniruotė"
        verbose_name_plural = "Treniruotės"


class Booking(models.Model):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    class_session = models.ForeignKey("Class", on_delete=models.CASCADE, null=True, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.member} for {self.class_session.name}"

    class Meta:
        verbose_name = "Registracija"
        verbose_name_plural = "Registracijos"


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=50, choices=[
        ('cardio', 'Cardio'),
        ('strength', 'Strength'),
        ('free weights', 'Free Weights')
    ])
    sport_hall = models.ForeignKey("SportHall", on_delete=models.CASCADE,
                                   limit_choices_to={'hall_type': 'treniruokliu'})
    purchase_date = models.DateField()
    condition = models.CharField(max_length=30, choices=[
        ('naujas', 'Naujas'),
        ('geras', 'Geras'),
        ('reikalauja aptarnavimo', 'Reikalauja aptarnavimo')
    ])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Treniruoklis"
        verbose_name_plural = "Treniruokliai"
