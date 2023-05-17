from django.urls import path
from . import views
from .views import StripeWebhookView

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('connect-store', views.connect_store, name='connect-store'),
    path('reset-store', views.reset_store, name='reset-store'),

    #path('pricing', views.pricing, name='pricing'),
    path('create-checkout-session', views.create_checkout_session, name='create-checkout-session'),
    path('payment-success', views.payment_success, name='payment-success'),
    path('payment-cancel', views.payment_cancel, name='payment-cancel'),
    path("webhooks/stripe/", StripeWebhookView.as_view(), name="stripe-webhook"), 

    # DASHBOARD
    #path('dashboard', views.dashboard, name='dashboard'),
    

    # INVENTORY LIST VIEW 
    path('inventory-list-view-manipulation-commands', views.inventory_list_view_manipulation_commands, name='inventory-list-view-manipulation-commands'),
    path('inventory-list-view-import-commands', views.inventory_list_view_import_commands, name='inventory-list-view-import-commands'),
    path('inventory-list-view-sync-commands', views.inventory_list_view_sync_commands, name='inventory-list-view-sync-commands'),
    path('inventory-list-view-delete/<int:pk>', views.inventory_list_view_delete, name='inventory-list-view-delete'),

    # INVENTORY ITEM DETAIL VIEW
    path('inventory-item-detail-view/<int:pk>', views.inventory_item_detail_view, name='inventory-item-detail-view'),
    path('inventory-item-detail-view/inventory-item-remove-image', views.inventory_item_remove_image, name='inventory-item-remove-image'),
    path('inventory-item-detail-view/inventory-item-set-main-image', views.inventory_item_set_main_image, name='inventory-item-set-main-image'),
    path('inventory-item-detail-view/inventory-item-detail-view-save-changes', views.inventory_item_detail_view_save_changes, name='inventory-item-detail-view-save-changes'),
    path('inventory-item-detail-view/inventory-item-detail-view-save-main-AI-manual-changes', views.inventory_item_detail_view_save_main_AI_manual_changes, name='inventory-item-detail-view-save-main-AI-manual-changes'),
    path('inventory-item-search-similar-items', views.inventory_item_search_similar_items, name='inventory-item-search-similar-items'),

    

    path('inventory-sync', views.inventory_sync, name='inventory-sync'),    
    
]