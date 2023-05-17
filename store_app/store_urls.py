
from django.urls import path
from . import views



urlpatterns = [
    path('store-onsale', views.store_onsale, name='store-onsale'),
    path('store-delete', views.store_delete, name='store-delete'),
    path('return-page/', views.return_page, name='return-page'),
    path('callback-endpoint/', views.callback_endpoint, name='callback-endpoint'),
    path('callback-endpoint-wc/', views.callback_endpoint_wc, name='callback-endpoint'),
        path('inventory-list-view', views.inventory_list_view, name='inventory-list-view'),

]