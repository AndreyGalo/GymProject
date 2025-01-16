from datetime import timedelta

from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Member, MembershipPlan, MembershipPurchase


# Sukurus vartotoją automatiskai sukuriamas ir narys(Member).
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        default_membership = MembershipPlan.objects.get(name="Paprastas")
        Member.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
            membership_type=default_membership
        )


# Per admin istrynus NARY(Member) issitrina ir user
@receiver(post_delete, sender=Member)
def delete_user_with_member(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()


# Pakeitus user vartotoja automatiskai pasikeicia nario(member) profilis.
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.member.save()


# Pridejus/Pakeitus Narystes PIRKIMA automatiskai priskiria nauja Naryste vartotojui(Member)
@receiver(post_save, sender=MembershipPurchase)
def update_member_membership(sender, instance, **kwargs):
    member = instance.member
    if member:
        # Atnaujiname narystės tipą Member modelyje pagal paskutinį MembershipPurchase
        member.membership_type = instance.membership_plan
        member.save()


# Narystes pirkimas arba per admino pridejimas(narystes pirkima) automatiskai priskria 30 dienu
@receiver(post_save, sender=MembershipPurchase)
def set_end_date(sender, instance, created, **kwargs):
    if created and not instance.end_date:
        instance.end_date = instance.start_date + timedelta(days=30)
        instance.save()


# Narystes PIRKIMO pasalinimas per admino puslapi automatiskai priskiria Paprasta naryste
@receiver(post_delete, sender=MembershipPurchase)
def remove_membership_from_member(sender, instance, **kwargs):
    member = instance.member
    default_membership = MembershipPlan.objects.get(name="Paprastas")
    if member:
        member.membership_type = default_membership
        member.save()
