from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

]