from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('faq', views.faq, name='faq'),
    path('contact', views.contact, name='contact'),
    path('whitelist', views.whitelist, name='whitelist'),
    path('terms-and-conditions', views.terms_and_conditions, name='terms-and-conditions'),

]