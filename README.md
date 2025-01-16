# GymProject

1. Apie:

Sporto salių komplekso aptarnavimo puslapis su duomenų baze, valdančia narius, narystės planus, treniruotes,
instruktorius, įrangą ir užsakymus.

2. Paleidimo instrukcijos:

Įdiekite reikalingas bibliotekas per terminalą:

    pip install -r requirements.txt

Sukurkite duomenų bazę per terminalą:

    python.exe .\manage.py makemigrations 
    python.exe .\manage.py migrate

Sukurkite supervartotoją per terminalą:

    python.exe .\manage.py createsuperuser

Atidarom Django interaktyvų aplinkos langą:

    python.exe .\manage.py shell

Importuojame modelius ir supervartotoją:

    from django.contrib.auth.models import User
    from gympro.models import Member, MembershipPlan

Gaunam supervartotoją:

    user = User.objects.first()

Sukuriame narystės planą, kuris automatiškai priskiriamas per signalą naujai sukurtiems nariams:

    plan = MembershipPlan.objects.create(
    name='Paprastas',  
    description='Paprasto plano aprašymas',
    monthly_fee=00.00,
    access_level='paprastas'
    )

Sukuriame MEMBER objektą supervartotojui:

    member = Member.objects.create(
    user=user,
    first_name='Jonas',
    last_name='Petras',
    email='jonas@example.com',
    membership_type=plan 
    )

Galutinis paleidimas:

    python.exe .\manage.py runserver (prisijungiam su admin,taip-pat pabandom uzregistruoti nauja vartotoja)

3. Kontaktai:
   galustyan.andrew@gmail.com
   https://github.com/AndreyGalo

