from django.urls import path
from . import views



urlpatterns = [
    # SMAARTCOPY
    path('smartcopy-start', views.smartcopy_start, name='smartcopy-start'),
    path('smartcopy-play', views.smartcopy_play, name='smartcopy-play'),
    path('smartcopy-write', views.smartcopy_write, name='smartcopy-write'),
    
    

    #path('woocommerce-update-descriptions-bulk', views.woocommerce_update_descriptions_bulk, name='woocommerce-update-descriptions-bulk'),
    path('generate-img', views.generate_img, name='generate-img'),
    path('generate-img-page', views.generate_img_page, name='generate-img-page'),
]