from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('connect-store', views.connect_store, name='connect-store'),
    path('reset-store', views.reset_store, name='reset-store'),

    # TRENDING
    path('trending', views.trending, name='trending'),

    # DASHBOARD
    #path('dashboard', views.dashboard, name='dashboard'),
    
    # SEARCH + RESULTS + IMPORT VIEWS
    path('search', views.search, name='search'),
    path('search-results', views.search_results, name='search-results'),
    path('search-product-details', views.search_product_details, name='search-product-details'),
    path('inventory-import', views.inventory_import, name='inventory-import'),

    # INVENTORY LIST VIEW 
    path('inventory-list-view', views.inventory_list_view, name='inventory-list-view'),
    path('inventory-list-view-manipulation-commands', views.inventory_list_view_manipulation_commands, name='inventory-list-view-manipulation-commands'),
    path('inventory-list-view-import-commands', views.inventory_list_view_import_commands, name='inventory-list-view-import-commands'),
    path('inventory-list-view-sync-commands', views.inventory_list_view_sync_commands, name='inventory-list-view-sync-commands'),

    # INVENTORY ITEM DETAIL VIEW
    path('inventory-item-detail-view/<int:pk>', views.inventory_item_detail_view, name='inventory-item-detail-view'),
    path('inventory-item-detail-view/inventory-item-remove-image', views.inventory_item_remove_image, name='inventory-item-remove-image'),
    path('inventory-item-detail-view/inventory-item-set-main-image', views.inventory_item_set_main_image, name='inventory-item-set-main-image'),
    path('inventory-item-detail-view/inventory-item-detail-view-save-changes', views.inventory_item_detail_view_save_changes, name='inventory-item-detail-view-save-changes'),
    path('inventory-item-detail-view/inventory-item-detail-view-save-main-AI-manual-changes', views.inventory_item_detail_view_save_main_AI_manual_changes, name='inventory-item-detail-view-save-main-AI-manual-changes'),
    path('inventory-item-detail-view/inventory-item-search-similar-items', views.inventory_item_search_similar_items, name='inventory-item-search-similar-items'),
    path('inventory-item-detail-view/gpt-generate-description', views.gpt_generate_description, name='gpt-generate-description'),
    path('inventory-item-detail-view/inventory-item-save-gpt-title', views.inventory_item_save_gpt_title, name='inventory-item-save-gpt-title'),
    path('inventory-item-detail-view/inventory-item-save-gpt-description', views.inventory_item_save_gpt_description, name='inventory-item-save-gpt-description'),
    
    # WOOCOMMERCE
    path('woocommerce-categories', views.woocommerce_categories, name='woocommerce-categories'),
    path('woocommerce-onsale', views.woocommerce_onsale, name='woocommerce-onsale'),

    # SHOPIFY
    path('shopify-onsale', views.shopify_onsale, name='shopify-onsale'),
    

    path('inventory-sync', views.inventory_sync, name='inventory-sync'),

    path('inventory-edit-items', views.inventory_edit_items, name='inventory-edit-items'),
    path('json-export-generate', views.inventory_import, name='json-export-generate'),

    # EBAY
    path('ebay-connect-store', views.ebay_connect_store, name='ebay-connect-store'),
    path('ebay-update-access-token', views.ebay_update_access_token, name='ebay-update-access-token'),
    path('ebay-start-export-batch', views.ebay_start_export_batch, name='ebay-start-export-batch'),
    path('ebay-inventory', views.ebay_inventory, name='ebay-inventory'),
    path('ebay-delete-inventory-items', views.ebay_delete_inventory_items, name='ebay-delete-inventory-items'),

    # SOCIAL
    path('social-settings', views.social_settings, name='social-settings'),
    path('social-instagram', views.social_instagram, name='social-instagram'),
    path('social-facebook', views.social_facebook, name='social-facebook'), 

    # FACEBOOK - INSTAGRAM
    path('facebook-login', views.facebook_login, name='facebook-login'),
    path('facebook-update-connection', views.facebook_update_connection, name='facebook-update-connection'),    
    path('instagram-create-post', views.instagram_create_post, name='instagram-create-post'),
    
    # PRINTFUL
    path('printful-oauth', views.printful_oauth, name='printful-oauth'),

    # UPDATE WORDS
    path('update-user-words', views.update_user_words, name='update-user-words'),

    # SMAARTCOPY
    path('smartcopy-start', views.smartcopy_start, name='smartcopy-start'),
    path('smartcopy-play', views.smartcopy_play, name='smartcopy-play'),
    
    

    #path('woocommerce-update-descriptions-bulk', views.woocommerce_update_descriptions_bulk, name='woocommerce-update-descriptions-bulk'),
    path('generate-img', views.generate_img, name='generate-img'),


    path('return-page', views.profile, name='return-page'),
    path('callback-endpoint', views.callback_endpoint, name='callback-endpoint'),
    
    
]