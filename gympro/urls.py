from django.urls import path

from gympro import views

urlpatterns = [
    path('', views.index, name='index'),
    path('apiemus/',views.apiemus,name="apiemus"),
    path('treneriai/',views.treneriai,name="treneriai"),
    path('treneris/<int:instructor_id>/', views.treneris, name='treneris'),
    path('tvarkarastis/', views.tvarkarastis_view, name='tvarkarastis'),
    path('sporto-sales/', views.sportosales, name='sporto_sales'),
    path('sporto-sale/<int:sporthall_id>/', views.sportosale, name='sporto_sale'),
    path('narystes/', views.narystes, name='narystes'),
    path('pirkti-naryste/<int:narystes_id>/', views.pirkti_naryste, name='pirkti_naryste'),
    path('patvirtinti-pirkima/<int:narystes_id>/', views.patvirtinti_pirkima, name='patvirtinti_pirkima'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('manotreniruotes/', views.manotreniruotes, name='manotreniruotes'),
    path('register-class/<int:class_id>/', views.register_class, name='register_class'),
    path('unregister-class/<int:class_id>/', views.unregister_class, name='unregister_class'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('unregister-success/', views.unregister_success, name='unregister_success'),
    path('unregister-denied/',views.unregister_denied,name='unregister_denied'),
    path('already-registered/', views.already_registered, name='already_registered'),
    path('korteles-apmokejimas/<int:narystes_id>/', views.korteles_apmokejimas, name='korteles_apmokejimas'),
    path('payment-success/<int:narystes_id>/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    path('treniruokliai/', views.treniruokliai, name='treniruokliai'),
]