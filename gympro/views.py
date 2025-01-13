from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.utils.timezone import localtime, now
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect

from .models import Instructor, Class, SportHall, MembershipPlan, Booking


def index(request):
    instruktoriai = Instructor.objects.all().count()
    context = {
        'instruktoriai': instruktoriai,
    }
    return render(request, "index.html", context=context)


def apiemus(request):
    return render(request, "apiemus.html")


def treneriai(request):
    treneriai = Instructor.objects.all()
    context = {'treneriai': treneriai, }
    return render(request, "treneriai.html", context=context)


def treneris(request, instructor_id):
    treneris = get_object_or_404(Instructor, pk=instructor_id)
    trenerio_tvarkarastis = treneris.classes.filter(schedule__gte=now()).order_by('schedule')
    context = {
        "treneris": treneris,
        "trenerio_tvarkarastis": trenerio_tvarkarastis,
    }
    return render(request, "treneris.html", context=context)


def sportosales(request):
    sales = SportHall.objects.all()
    context = {'sales': sales, }
    return render(request, "sporto_sales.html", context=context)


def sportosale(request, sporthall_id):
    sale = get_object_or_404(SportHall, pk=sporthall_id)
    sales_tvarkarastis = sale.classes.filter(schedule__gte=now()).order_by('schedule')
    context = {
        "sale": sale,
        "sales_tvarkarastis": sales_tvarkarastis,
    }
    return render(request, "sporto_sale.html", context=context)


def narystes(request):
    narystes = MembershipPlan.objects.filter(access_level__in=['premium', 'platinum']).order_by(
        'monthly_fee')
    context = {'narystes': narystes, }
    return render(request, "narystes.html", context=context)


def tvarkarastis_view(request):
    """
    classes filtruojam turimam Class modelyje nustatytas pagal datas treniruotes --
    kur: date_GREATER THAN OR EQUAL(Django ORM Filters)=today(siandienos data).
    for ciklas,iteruojam per turimas treniruotes musu classes sarase
    ir pridedam i nauja sarasa/kintamaji schedule pakeistu datos,laiko formatu ir tiksliu treniruoes pavadinimu(name)

    """
    classes = Class.objects.filter(schedule__gte=now()).order_by('schedule')
    paginator = Paginator(classes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    schedule = []
    for treniruote in page_obj:
        local_schedule = localtime(treniruote.schedule)
        schedule.append({
            'id': treniruote.id,
            'date': local_schedule.date().strftime("%Y.%m.%d"),
            'time': local_schedule.time().strftime("%H:%M"),
            'name': treniruote.name,
            'coach_pavarde': treniruote.instructor.last_name,
            'coach_vardas': treniruote.instructor.first_name,
            'is_full': treniruote.is_full,
            'coach_id': treniruote.instructor.id,
        })

    context = {
        'schedule': schedule,
        'page_obj': page_obj,
    }

    return render(request, 'tvarkarastis.html', context=context)


@csrf_protect
def register(request):
    """
    Registracijos funkcija su slaptažodžio patikrinimu ir privalomais laukais.
    """
    if request.method == "POST":
        # Pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Patikriname, ar visi laukai užpildyti
        if not username or not first_name or not last_name or not email or not password or not password2:
            messages.error(request, "Visi laukai turi būti užpildyti!")
            return redirect('register')

        # Tikriname, ar sutampa slaptažodžiai
        if password != password2:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')

        # Tikriname slaptažodį pagal nustatytus validatorių reikalavimus
        try:
            validate_password(password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect('register')

        # Tikriname, ar vartotojo vardas užimtas
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Vartotojo vardas {username} užimtas!')
            return redirect('register')

        # Tikriname, ar el. paštas jau naudojamas
        if User.objects.filter(email=email).exists():
            messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
            return redirect('register')

        # Jei viskas tvarkoje, sukuriame naują vartotoją
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        messages.success(request, f'Vartotojas {username} užregistruotas!')
        return redirect('login')

    return render(request, 'register.html')


@login_required
def profile(request):
    member = request.user.member
    bookings = Booking.objects.filter(member=member, class_session__schedule__gte=now()).order_by(
        'class_session__schedule')
    membership_purchase = member.purchases.order_by('-start_date').first()
    membership_photo = member.membership_type.photo
    context = {
        'member': member,
        'bookings': bookings,
        'membership_purchase': membership_purchase,
        'membership_photo': membership_photo,
    }
    return render(request, 'accounts/profile.html', context=context)


@login_required
def register_class(request, class_id):
    klase = get_object_or_404(Class, pk=class_id)
    member = request.user.member  # Kiekvienas vartotojas turi Member objektą

    if Booking.objects.filter(member=member, class_session=klase).exists():
        return redirect('already_registered')

    Booking.objects.create(member=member, class_session=klase)
    klase.current_bookings += 1
    klase.save()
    return redirect('registration_success')


def registration_success(request):
    return render(request, 'registration_success.html')


def already_registered(request):
    return render(request, 'already_registered.html')


@login_required
def unregister_class(request, class_id):
    member = request.user.member
    klase = get_object_or_404(Class, id=class_id)
    booking = Booking.objects.filter(member=member, class_session=klase).first()

    # Patikriname, ar iki treniruotės pradžios liko daugiau nei 24 valandos
    if klase.schedule - now() < timedelta(hours=24):
        return redirect('unregister_denied')

    # Pašaliname registraciją
    booking.delete()
    klase.current_bookings -= 1
    klase.save()
    return redirect('unregister_success')


def unregister_success(request):
    return render(request, 'unregister_success.html')


def unregister_denied(request):
    return render(request, 'unregister_denied.html')
