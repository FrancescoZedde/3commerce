from django.urls import path
from . import views



urlpatterns = [

    path('social-settings', views.social_settings, name='social-settings'),
    path('social-instagram', views.social_instagram, name='social-instagram'),
    path('social-facebook', views.social_facebook, name='social-facebook'), 
    path('facebook-login', views.facebook_login, name='facebook-login'),
    path('facebook-update-connection', views.facebook_update_connection, name='facebook-update-connection'),    
    path('instagram-create-post', views.instagram_create_post, name='instagram-create-post'),

]