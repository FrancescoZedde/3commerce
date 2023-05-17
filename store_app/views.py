from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from store_app.store_woocommerce import WooCommerce, WooCommerceConnect, woocommerce_retrieve_product_by_id
from store_app.store_shopify import Shopify, ShopifyConnect, shopify_exchange_code


from main_app.models import InventoryItem

# Create your views here.
@login_required(login_url='/login')
def store_onsale(request):
    if request.method == 'GET':
        #check if store is woo or shop
        user_instance = CustomUser.objects.get(email=request.user.email)
        print(user_instance.store_type)
        if user_instance.store_type == 'shopify':
            class_instance = Shopify(user_instance)
            products = Shopify.shopify_retrieve_all_products(class_instance)
            print(products)
            list_products = []
            for product in products:
                list_products.append(map_json_shopify_to_woocommerce(product))
            print('heere')
            context = {'products': list_products}
            return render(request, 'main_app/store_onsale.html', context)
        elif user_instance.store_type == 'woocommerce':
            class_instance = WooCommerce(request.user)
            woocommerce_products = WooCommerce.woocommerce_retrieve_limited_products(class_instance)
            print(woocommerce_products)
            products = make_woocommerce_on_sale_products_list(woocommerce_products)
            print(products)
            context = {
                   'products': products,
                    }
            return render(request, 'main_app/store_onsale.html', context)
        else:
            return redirect(inventory_list_view)
    if request.method == 'POST':
        return redirect(inventory_list_view)


@login_required(login_url='/login')
def store_delete(request):
    if request.method=='GET':
        return redirect(store_onsale)
    if request.method =='POST':
        store_id = request.POST.get("store-product-id", None)
        force = request.POST.get("force", False)
        if force == "on" or force == True:
            force = 'true'
        elif force == None or force == False:
            force = 'false'
        else:
            force = 'false'

        
        print(store_id)
        #check store type
        store_type = request.user.store_type
        if store_type == 'shopify':
            print("shop")
        elif store_type == 'woocommerce':
            print("shop")
            try:
                class_instance = WooCommerce(request.user)
                response = WooCommerce.woocommerce_delete_product(class_instance, store_id, force)
                print(response)
                messages.success(request, f'Product removed!')
                return redirect(store_onsale)
            except:
                messages.error(request, f'Error, note deleted')
                return redirect(store_onsale)



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
def inventory_list_view(request):
    if request.method == 'GET':

        products = InventoryItem.objects.filter(user=request.user)
        products = reversed(products)
        print('All products associated with logged user: ')
        print(products)

        context = {
            'all_inventory_items' : products,
            'show_select_all' : 'true',

        }
        return render(request, 'store_app/inventory_list_view.html', context)