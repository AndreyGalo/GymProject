from django.urls import path

from gympro import views

urlpatterns = [
    path('', views.index, name='index'),
    path('apiemus/',views.apiemus,name="apiemus"),
    path('treneriai/',views.treneriai,name="treneriai"),
    path('treneris/<int:instructor_id>/', views.treneris, name='treneris'),
    path('tvarkarastis/', views.tvarkarastis_view, name='tvarkarastis'),
    path('sporto_sales/', views.sportosales, name='sporto_sales'),
    path('narystes/', views.narystes, name='narystes'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('register-class/<int:class_id>/', views.register_class, name='register_class'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('already-registered/', views.already_registered, name='already_registered'),
]