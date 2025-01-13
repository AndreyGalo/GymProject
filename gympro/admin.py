from django.utils import timezone
from django.utils.timezone import localtime

from django.contrib import admin
from .models import Class, Booking, Equipment, Member, MembershipPlan, Instructor, SportHall, MembershipPurchase


class ClassAdmin(admin.ModelAdmin):
    list_display = (
    "name", "class_type", "instructor", "sport_hall", "formatted_schedule", "max_capacity", "current_bookings")
    ordering = ('schedule',)
    def formatted_schedule(self, obj):
        # Naudojame localtime, kad parodytume teisingą laiką pagal nustatytą laiko zoną
        return localtime(obj.schedule).strftime('%Y-%m-%d %H:%M')

    formatted_schedule.admin_order_field = 'schedule'


class BookingAdmin(admin.ModelAdmin):
    list_display = ("member", "class_session", "booking_date")


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "equipment_type", "sport_hall", "purchase_date", "condition")


class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "user", "first_name", "last_name", "email", "phone_number", "join_date", "membership_type", "active")
    readonly_fields = ('membership_type',)


class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name", "description", "monthly_fee", "access_level")


class MembershipPurchaseAdmin(admin.ModelAdmin):
    list_display = ("member", "membership_plan", "start_date", "end_date")


class InstructorAdmin(admin.ModelAdmin):
    list_display = (
        "first_name", "last_name", "specialization", "bio", "contact_email", "phone_number", "instagram", "facebook",
        "linkedin")


class SportHallAdmin(admin.ModelAdmin):
    list_display = ("name", "hall_type", "capacity")


admin.site.register(Class, ClassAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(MembershipPlan, MembershipPlanAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(SportHall, SportHallAdmin)
admin.site.register(MembershipPurchase, MembershipPurchaseAdmin)
