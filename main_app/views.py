from django.shortcuts import render, redirect
from ast import literal_eval
from django.http import HttpResponse
import json
import re
import pandas as pd
from urllib.parse import unquote
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from urllib.parse import urlencode
from django.urls import reverse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View



import stripe



from main_app.views_utils import set_null_if_missing,check_order, map_json_shopify_to_woocommerce, new_default_template, format_results, woocommerce_extract_text_description, woocommerce_get_first_10_images, make_woocommerce_on_sale_products_list, remove_img_tags, clean_html,create_template_description_string, make_sku_list, create_default_template_description_string, filter_by_keywords, create_item_and_variants_forms


from main_app.forms import CJSearchProducts, exportSetup, InventoryItemForm, VariantForm, newStoreWoocommerce, woocommerceImportSetup, InstagramPostSetup

from main_app.models import InventoryItem, Variant

from main_app.ws_serpapi import SerpApi

from main_app.db_functions import convert_shopify_woocommerce_products_in_standard_format, update_user_searches, retrieve_last_user_order, create_contract_order, save_checkout_session, reset_cjdropshipping, updateUserWords, retrieveVariantsByItem, connect_cj_account, retrieveItemBySku, connect_shopify_store, reset_shopify_store, reset_woocommerce_store, connect_woocommerce_store, deleteItemBySku, retrieveAllInventoryItems,update_variant, retrieveInventoryItemById, create_item_and_variants,update_items_offer,update_item



from users_app.models import CustomUser, Order
from users_app.forms import WooCommerceConnectForm, ShopifyConnectForm, CJDropshippingConnectForm


from django.http import JsonResponse



def pricing(request):
    if request.method == 'GET':

        return render(request, 'main_app/pricing.html')
    if request.method == 'POST':

        return render(request, 'main_app/pricing.html')



@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            print("Payment successful")
            print(event)
            print(type(event))
            save_checkout_session(event)
            print('ijnxj')

        # Can handle other events here.

        return HttpResponse(status=200)


def create_checkout_session(request):
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        print(request.POST['lookup_key'])
        prices = stripe.Price.list(
            lookup_keys=[request.POST['lookup_key']],
            expand=['data.product']
        )
        #prices = stripe.Price.list(limit=3)
        print(prices)
        if request.POST['lookup_key'] in ['words-10k','words-25k','words-100k']:
            mode = 'payment'
        else:
            mode = 'subscription'
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': prices['data'][0]['id'],
                    'quantity': 1,
                },
            ],
            mode=mode,
            success_url='http://127.0.0.1:8000' +
            '/payment-success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000' + '/payment-cancel',
        )

        create_contract_order(request.user, request.POST['lookup_key'])

        return redirect(checkout_session.url, code=303)
    except Exception as e:
        print(e)
        return redirect(pricing)


@login_required(login_url='/login')
def payment_success(request):
    if request.method == 'GET':
        user_instance = request.user
        last_order = retrieve_last_user_order(user_instance)
        print(last_order.lookup_key)
        if last_order.lookup_key == 'starter-month' or last_order.lookup_key == 'starter-year':
            user_instance.status = 'basic'
            user_instance.save()
        elif last_order.lookup_key == 'business-month' or last_order.lookup_key == 'business-year':
            user_instance.status = 'premium'
            user_instance.save()
        else:
            user_instance.status = 'free'
            user_instance.save()
            
        session_id = request.GET.get('session_id')    
        print(session_id)
        messages.success(request, f'Paymente completed!')
        return redirect(pricing)

@login_required(login_url='/login')
def payment_cancel(request):
    if request.method == 'GET':
        messages.error(request, f'Payment failed! Try again or contact Support')
        return redirect(pricing) 


def callback_endpoint_wc(request):
    if request.method == 'GET':
        print('get request callback')
        code = 'test'
        return JsonResponse({'message': 'API keys received', 'code':code })
    if request.method == 'POST':
        print('here')
        data = request.POST.get('data')
        # Save the data to your database
        print(data)
        return JsonResponse({'message': 'API keys received'})
    else:
        return JsonResponse({'error': 'Invalid request'})



def callback_endpoint(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        #hmac = request.GET.get('hmac')
        host = request.GET.get('host')
        shop = request.GET.get('shop')
        #timestamp = request.GET.get('timestamp')
        try:
            response = shopify_exchange_code(shop, code)
            # save access-token for the user
            access_token = response['access_token']
            user_instance = CustomUser.objects.get(email=request.user.email)
            user_instance.store_type = 'Shopify'
            user_instance.store_name = shop
            user_instance.shopify_secret_key = access_token
            user_instance.shopify_host = 'https://' + str(shop)
            user_instance.shopify_store_name = shop
            user_instance.save()

            # sync store / donload products
            class_instance = Shopify(user_instance)
            response = Shopify.shopify_retrieve_orders(class_instance)
            data = Shopify.shopify_retrieve_all_products(class_instance)
            print(data)
            convert_shopify_woocommerce_products_in_standard_format('shopify', data)
            

            messages.success(request, f"Success, Shopify store connected!")
            return redirect(profile)

        except:
            messages.error(request, f"Something goes wrong, retry or contact support.")
            return redirect(profile)
    if request.method == 'POST':
        return redirect(profile)
    else:
        return redirect(profile)

def return_page(request):
    if request.method == 'GET':
        print('get here')
        return JsonResponse({'message': 'API keys GET'})
    if request.method == 'POST':
        
        return JsonResponse({'message': 'API keys POST'})
    else:
        return JsonResponse({'error': 'Invalid request'})

@login_required(login_url='/login')
def profile(request):
    if request.method == 'GET':

        store_url = 'https://xzshop.eu'
        endpoint = '/wc-auth/v1/authorize'


        params = {
            "app_name": "SellFastApp",
            "scope": "read_write",
            "user_id": 123,
            "return_url": 'http://sellfast.app'  + '/return-page',
            "callback_url": 'https://sellfast.app' + '/callback-endpoint-wc'
        }
        query_string = urlencode(params)
        print(params)
        print("%s%s?%s" % (store_url, endpoint, query_string))

        #auth_url = store_url + endpoint + query_string
        #print(auth_url)

        auth_url = "%s%s?%s" % (store_url, endpoint, query_string)


        shopify_store_url = "https://sellfast-development-store.myshopify.com/admin/oauth/authorize"
        shopify_params = {
            "client_id": "700418a025a1df4a02784f0ed03362da",
            "scope": "write_products, read_orders, orders, marketplace_orders",
            "redirect_uri" : "https://sellfast.app/callback-endpoint"
        }

        shopify_query_string = urlencode(shopify_params)
        shopify_auth_url = "%s?%s" % (shopify_store_url, shopify_query_string)

        print(shopify_auth_url)
        woocommerce_connect = WooCommerceConnectForm()
        shopify_connect = ShopifyConnectForm()
        cjdropshipping_connect = CJDropshippingConnectForm()

        context = {
            'shopify_auth_url':shopify_auth_url,
            'auth_url':auth_url,
            'woocommerce_connect':woocommerce_connect,
            'shopify_connect': shopify_connect,
            'cjdropshipping_connect':cjdropshipping_connect,
        }
        return render(request, 'main_app/profile.html', context)




@login_required(login_url='/login')
def connect_store(request):
    if request.method == 'GET':
        return redirect(profile)
    if request.method == 'POST':
        connect_to = request.POST.get("connect", None)
        print(request.POST)
        if connect_to == "woocommerce":
            try:
                store_name = request.POST.get("woocommerce_store_name",None)
                domain = request.POST.get("woocommerce_host",None)
                ck = request.POST.get("woocommerce_consumer_key",None)
                cs = request.POST.get("woocommerce_secret_key",None)
                connection = WooCommerceConnect(domain, ck, cs)
                if connection.status == "valid":
                    connect_woocommerce_store(request.user,store_name, domain, ck, cs)
                    messages.success(request, f"Success, WooCommerce store connected!")
                else:
                    messages.error(request, f"Connection failed: invalid credentials. Retry or contact support")
                return redirect(profile)
            except:
                messages.error(request, f"Somethin goes wrong, contact Support")
                return redirect(profile)
        elif connect_to == "shopify":
            try:
                store_name = request.POST.get("shopify_store_name",None)
                shopify_store_url = "https://" + str(store_name) +".myshopify.com/admin/oauth/authorize"
                shopify_params = {
                    "client_id": "700418a025a1df4a02784f0ed03362da",
                    "scope": "write_products, read_orders, write_orders",
                    "redirect_uri" : "https://sellfast.app/callback-endpoint"
                }

                print("here1")
                shopify_query_string = urlencode(shopify_params)
                shopify_auth_url = "%s?%s" % (shopify_store_url, shopify_query_string)
                #auth_url = shopify_build_auth_url()
                
                return redirect(str(shopify_auth_url))
                
                '''
                if connection.status == "valid":
                    connect_shopify_store(request.user,store_name, domain, ck, cs)
                    messages.success(request, f"Success, Shopify store connected!")
                else:
                    messages.error(request, f"Connection failed: invalid credentials. Retry or contact support")
                return redirect(profile)'''
            except:
                messages.error(request, f"Somethin goes wrong, contact Support")
                return redirect(profile)
        elif connect_to == "cjdropshipping":
            try:
                print("connect to cjdropshipping ...")
                cj_email = request.POST.get("cjdropshipping_email",None)
                cj_key = request.POST.get("cjdropshipping_api_key",None)

                connection = CJDropshippingConnect(cj_email, cj_key)
                if connection.status == "valid":
                    connect_cj_account(request.user, cj_email, cj_key)
                    messages.success(request, f"Success, CJ Dropshipping account connected!")
                else:
                    messages.error(request, f"Connection failed: invalid credentials. Retry or contact support")
                return redirect(profile)
            except:
                messages.error(request, f"Somethin goes wrong, contact Support")
                return redirect(profile)
        else:
            return redirect(profile)


@login_required(login_url='/login')
def reset_store(request):
    if request.method == 'GET':
        return redirect(profile)
    if request.method == 'POST':
        reset = request.POST.get("reset", None)
        if reset == 'woocommerce':
            reset_woocommerce_store(request.user)
            reset_shopify_store(request.user)
        elif reset == 'shopify':
            reset_shopify_store(request.user)
            reset_woocommerce_store(request.user)
        elif reset == 'cjdropshipping':
            reset_cjdropshipping(request.user)
        return redirect(profile)




@login_required(login_url='/login')
def inventory_list_view_manipulation_commands(request):
    if request.method == 'GET':
        return redirect(inventory_list_view)
    if request.method == 'POST':
        dropdown_value = request.POST.get("action", 'none')
        selected_items = request.POST.get("selected-items", None)
        selected_items = re.split(',', selected_items,)
        if dropdown_value == 'edit':
            print('do edit')
        elif dropdown_value == 'add-description':
            print('add-description')
            items = InventoryItem.objects.filter(user=request.user, sku__in=selected_items)
            model = request.POST.get("model", None)
            keywords = request.POST.get("keywords", '')
            min_words = request.POST.get("min_words", 80)
            max_words = request.POST.get("max_words", 200)
            rewrite_title = request.POST.get("rewrite_title", None)
            class_instance = ChatGPT()
            for item in items:
                if model == 'gpt-3.5-turbo':
                    if rewrite_title != None:
                        chatgpt_title = ChatGPT.write_product_title(class_instance, item.itemName, item.categoryThird)
                        item.itemName = chatgpt_title
                        print('GPT Completition Title:')
                        print(chatgpt_title)
                    chatgpt_description = ChatGPT.gpt35_write_product_description(class_instance, item.itemName, clean_html(item.description), keywords, max_words, min_words)
                    item.descriptionCustom = chatgpt_description
                    print('GPT 3.5 Description:')
                    print(chatgpt_description)
                else:
                    if rewrite_title != None:
                        chatgpt_title = ChatGPT.write_product_title(class_instance, item.itemName, item.categoryThird)
                        item.itemName = chatgpt_title
                        print('GPT Completition Title:')
                        print(chatgpt_title)
                    chatgpt_description = ChatGPT.write_product_description(class_instance, model, item.itemName, item.description, keywords)
                    item.descriptionCustom = chatgpt_description
                    print('GPT Completition Description:')
                    print(chatgpt_description)
                item.save()
            return redirect(inventory_list_view)
        elif dropdown_value == 'add-template':
            for item_sku in selected_items:
                item = InventoryItem.objects.filter(user=request.user, sku=item_sku)
                new_default_template(item[0])
            return redirect(inventory_list_view)

        elif dropdown_value == 'add-description-and-template':
            print('do edit')

        elif dropdown_value == 'delete':
            items = InventoryItem.objects.filter(user=request.user, sku__in=selected_items)
            for item_sku in selected_items:
                message_result = deleteItemBySku(request.user, item_sku)
            return redirect(inventory_list_view)

        elif dropdown_value == 'none':
            messages.error(request, f"Select a valid option")
            return redirect(inventory_list_view)
             
    #MASS EDIT
    #print(request.POST)
    #MASS DELETE

    #MASS ADD TEMPLATE
    return redirect(inventory_list_view)

@login_required(login_url='/login')
def inventory_list_view_import_commands(request):
    print(request.POST)
    if request.method == 'GET':
        return redirect(inventory_list_view)
    if request.method == 'POST':
        dropdown_value = request.POST.get("action", 'none')
        selected_items = request.POST.get("selected-items", None)
        selected_items = re.split(',', selected_items,)
        if dropdown_value == 'import-shopify':
            print('import to shopify')
            print(selected_items)
            percentage_increase = request.POST.get("pricepercentageincrease", None)
            minimumprice = float(request.POST.get("minimumprice", None))
            roundat = request.POST.get("roundat", None)
            use_preset_price = request.POST.get("use_preset_price", None)
            print(use_preset_price)
            print(minimumprice)
            update_items_offer(request.user, selected_items, percentage_increase, minimumprice, roundat,use_preset_price)
            items = InventoryItem.objects.filter(user=request.user, sku__in=selected_items)
            for item in items:
                variants = Variant.objects.filter(item=item) 
                #Shopify.shopify_create_new_product(item, variants)
                class_instance = Shopify(request.user)
                create_product_response = Shopify.shopify_create_new_product(class_instance, item, variants)
                print(create_product_response)
                Shopify.shopify_add_images_to_variants(class_instance, variants, create_product_response)
            messages.error(request, f"Select a valid option + {create_product_response}")
            return redirect(inventory_list_view)
        elif dropdown_value == 'import-woocommerce':
            print("import to woocommerc")
            percentage_increase = request.POST.get("pricepercentageincrease", None)
            minimumprice = request.POST.get("minimumprice", None)
            roundat = request.POST.get("roundat", None)
            categories = request.POST.get("wc-categories", None)
            #select_categories = request.POST.get("selectcategories", None)

            selected_items = re.split(',', selected_items,)
            categories = re.split(',', categories,)
            print(categories)
            update_items_offer(request.user, selected_items, percentage_increase, minimumprice, roundat, use_preset_price)
            #start_woocommerce_products_batch(selected_items, categories)
            class_instance = WooCommerce(request.user)
            WooCommerce.start_woocommerce_products_batch(class_instance, selected_items, categories )
            return redirect(inventory_list_view)
        elif dropdown_value == 'import-ebay':
            return redirect(inventory_list_view)
        elif dropdown_value == 'none':
            return redirect(inventory_list_view)

@login_required(login_url='/login')
def inventory_list_view_sync_commands(request):
    print(request.POST)
    return redirect(inventory_list_view)

@login_required(login_url='/login')
def inventory_list_view_delete(request, pk):
    item = retrieveInventoryItemById(pk)
    item.delete()
    return redirect(inventory_list_view)

@login_required(login_url='/login')
def inventory_item_detail_view(request, pk):
    #inventory-item-detail-view
    print(pk)
    gpt_write_dscription_form = ChatGPTWriteDescriptionForm()
    item = retrieveInventoryItemById(pk)
    variants = retrieveVariantsByItem(item)
    class_instance = CJDropshipping(request.user)
    cj_access_token = CJDropshipping.cj_get_access_token(class_instance)
    #print(cj_access_token)
    item_original_description = remove_img_tags(item.description)
    img_set = literal_eval(item.productImageSet)
    item_form = InventoryItemForm(instance=item)

    variant_forms = []
    for variant in variants:
        variant_form = VariantForm(instance=variant)
        variant_forms.append(variant_form)

    context = {'pk': pk, 
                'item':item,
                'variants':variants,
                'item_form': item_form,
                'item_original_description':item_original_description,
                'img_set':img_set,
                'gpt_write_dscription_form': gpt_write_dscription_form,
                'cj_access_token':cj_access_token,
                }
    return render(request, 'main_app/inventory_item_detail_view.html', context)

@login_required(login_url='/login')
def inventory_item_detail_view_save_changes(request):
    if request.method == 'GET':
        return redirect(inventory_item_detail_view, pk=primary_key)
    elif request.method == 'POST':
        mode = request.POST.get("save-mode", None)
        primary_key = request.POST.get("primary-key", None)
        if mode == 'save-item':
            new_name = request.POST.get("itemName", None)
            new_sellprice= request.POST.get("sellPrice", None)
            new_custom_description = request.POST.get("descriptionCustom", None)
            item = retrieveInventoryItemById(primary_key)
            item.itemName = new_name
            item.sellPrice = new_sellprice
            item.descriptionCustom = new_custom_description
            item.save()
            messages.success(request, f'Item updated')
            return redirect(inventory_item_detail_view, pk=primary_key)
        elif mode == 'save-variant':
            print(request.POST)
            variant_id = request.POST.get("variant-id-update", None)
            new_name = request.POST.get("variantNameEn", None)
            new_sellprice = request.POST.get("sellPrice", None)
            variant = Variant.objects.get(id=variant_id)
            variant.variantNameEn = new_name
            variant.sellPrice = new_sellprice
            variant.save()
            messages.success(request, f'Variant updated')
            return redirect(inventory_item_detail_view, pk=primary_key)
        else:
            messages.error(request, f'Generic Error')
            return redirect(inventory_item_detail_view, pk=primary_key)

@login_required(login_url='/login')
def inventory_item_detail_view_save_main_AI_manual_changes(request):
    primary_key = request.POST.get("primary-key", None)
    new_descriptionCustom = request.POST.get("descriptionCustom", None)

    item = retrieveInventoryItemById(primary_key)
    item.descriptionCustom = new_descriptionCustom
    
    item.save()

    return redirect(inventory_item_detail_view, pk=primary_key)

@login_required(login_url='/login')
def inventory_item_remove_image(request):
    img_url = request.POST.get("img-url", None)
    primary_key = request.POST.get("primary-key", None)
    item = retrieveInventoryItemById(primary_key)
    img_set = literal_eval(item.productImageSet)
    img_set.remove(img_url)
    item.productImageSet = str(img_set)
    item.save()
    return redirect(inventory_item_detail_view, pk=primary_key)

@login_required(login_url='/login')
def inventory_item_set_main_image(request):
    img_url = request.POST.get("img-url", None)
    primary_key = request.POST.get("primary-key", None)
    item = retrieveInventoryItemById(primary_key)
    # set as main
    item.productImage = img_url

    # remove and re-add as first element in img set
    img_set = literal_eval(item.productImageSet)
    img_set.remove(img_url)
    img_set.insert(0, img_url)
    item.productImageSet = str(img_set)

    #save
    item.save()

    return redirect(inventory_item_detail_view, pk=primary_key)

@login_required(login_url='/login')
def inventory_item_search_similar_items(request):
    if request.method == 'GET':
        return render(request, 'main_app/inventory_item_search_similar_items.html', context)
    if request.method == 'POST':
        print(request.POST)
        
        search_by = request.POST.get("search-by", None)
        location = request.POST.get('similar-item-location', None)
        item_image = request.POST.get("item-image", None)
        item_name = request.POST.get("item-name", None)
        class_instance = SerpApi()
        if request.user.searches <= 0:
            messages.error(request, f"You've finished your words!")
            return redirect(inventory_item_detail_view, pk=primary_key)
        if search_by == 'item-name':
            
            shopping_results = SerpApi.serp_search_by_query(class_instance, item_name, location, 'en')
            ebay_results = SerpApi.serp_ebay_search_by_query(class_instance, item_name)
            #related_results = SerpApi.serp_search_related_results_query(class_instance, item.itemName, location, 'en')
            print('EBAY RESULTS')
            print(shopping_results)
            #shopping_results = related_results + shopping_results
            #print(ebay_results)
            update_user_searches(request.user)
            context = {'item_name': item_name,
            'item_image': item_image,
                    'shopping_results': shopping_results,
                    'ebay_results': ebay_results,
                    'search_by':search_by,
                    }
            return render(request, 'main_app/inventory_item_search_similar_items.html', context)
        elif search_by == 'item-image':
            inline_images = SerpApi.serp_reverse_image(class_instance, item_image)
            update_user_searches(request.user)
            context = {
                'item_name': item_name,
                'item_image': item_image,
                    'inline_images': inline_images,
                    'search_by':search_by,
                    }
            return render(request, 'main_app/inventory_item_search_similar_items.html', context)




@login_required(login_url='/login')
def inventory_sync(request):
    if request.method == 'GET':
        return redirect(inventory_list_view)
    if request.method == 'POST':
        #retireve app inventory items
        #all_inventory_items = retrieveAllInventoryItems()
        all_inventory_items = InventoryItem.objects.filter(user=request.user)
        #make list
        inventory_sku_list = make_sku_list(all_inventory_items, 'app-inventory')
        full_sync = request.POST.get('full-sync', None)
        print(full_sync)
        if request.user.store_type == 'woocommerce':

            print('START sync-with-woocommerce')
            class_instance = WooCommerce(request.user)
            woocommerce_items = WooCommerce.woocommerce_retrieve_all_products(class_instance)
            woocommerce_sku_list = make_sku_list(woocommerce_items, 'sync-woocommerce')
            context = {'results': results}
            return redirect(inventory_list_view)
        elif request.user.store_type == 'shopify':
            class_instance = Shopify(request.user)
            shopify_items = Shopify.shopify_retrieve_all_products(class_instance)
            convert_shopify_woocommerce_products_in_standard_format('shopify', shopify_items)
            results = ''
            context = {'results': results}
            return redirect(inventory_list_view)
        elif 'sync-with-ebay' in request.POST:
            print('START sync-with-ebay')
            '''
            #retrieve ebay items
            ebay_items = ebay_retrieve_all_products()
            #make list
            ebay_sku_list = make_sku_list(ebay_items, 'sync-ebay')
            #compare con inventory_sku_list
            results = compare_lists(inventory_sku_list, ebay_sku_list)'''

            return redirect(inventory_list_view)
        else:
            return redirect(inventory_list_view)



