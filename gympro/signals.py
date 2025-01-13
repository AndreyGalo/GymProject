from datetime import timedelta

from django.db.models.signals import post_save, post_delete  # signalas (būna įvairių)
from django.contrib.auth.models import User  # siuntėjas
from django.dispatch import receiver  # priėmėjas (dekoratorius)
from .models import Member, MembershipPlan, MembershipPurchase


# Sukurus vartotoją automatiskai sukuriamas ir narys(Member).
@receiver(post_save, sender=User)  # jeigu išsaugojamas User objektas, inicijuojama f-ja po dekoratoriumi
def create_profile(sender, instance, created, **kwargs):  # instance yra ką tik sukurtas User objektas.
    """
    default_membership kintamasis kuris pasiima Membershipplan objektus,suranda "Paprastas" naryste ir pasiima ja per GET metoda.
    objects.create sukurdamas priskiria Member modeliui membership_type paimta is GET metodo "Paprastas" naryste ir priskiria ja,naujai sukurtam vartotojui.
    """
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


# Pakeitus vartotoja automatiskai pasikeicia nario profilis.
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.member.save()


# Pridejus/Pakeitus Narystes PIRKIMA automatiskai priskiria nauja Naryste vartotojui(Member)
@receiver(post_save, sender=MembershipPurchase)
def update_member_membership(sender, instance, **kwargs):
    """
    Signalas atnaujina naryste `Member` modelyje po pakeitimo Admin puslapyje.
    """
    member = instance.member
    if member:
        # Atnaujiname narystės tipą Member modelyje pagal paskutinį MembershipPurchase
        member.membership_type = instance.membership_plan
        member.save()


# Narystes pirkimas arba per admino pridejimas automatiskai priskria 30 dienu
@receiver(post_save, sender=MembershipPurchase)
def set_end_date(sender, instance, created, **kwargs):
    if created and not instance.end_date:  # Tik naujai sukurtiems objektams
        instance.end_date = instance.start_date + timedelta(days=30)
        instance.save()


# Narystes pasalinimas per admino puslapi automatiskai priskiria Paprasta naryste
@receiver(post_delete, sender=MembershipPurchase)
def remove_membership_from_member(sender, instance, **kwargs):
    member = instance.member
    default_membership = MembershipPlan.objects.get(name="Paprastas")
    if member:
        member.membership_type = default_membership
        member.save()
