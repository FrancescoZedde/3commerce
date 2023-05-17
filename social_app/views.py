from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users_app.models import CustomUser

# Create your views here.

# SOCIAL NETWORK
@login_required(login_url='/login')
def social_settings(request):
    if request.method == 'GET':
        return render(request, 'main_app/social_settings.html')


@login_required(login_url='/login')
def social_instagram(request):
    if request.method == 'GET':
        return render(request, 'main_app/social_instagram.html')

@login_required(login_url='/login')
def social_facebook(request):
    if request.method == 'GET':
        return render(request, 'main_app/social_facebook.html')

@login_required(login_url='/login')
def facebook_login(request):
    if request.method == 'GET':
        return render(request, 'main_app/facebook_login.html')

@login_required(login_url='/login')
def facebook_update_connection(request):
    if request.method == 'POST':
        try:
            new_token = request.POST.get("new-access-token", None)
            fb_user_id = request.POST.get("fb-user-id", None)
            fb_page_id = request.POST.get("fb-page-id", None)
            ig_user_id = request.POST.get("ig-user-id", None)
            print('here')
            user_instance = CustomUser.objects.get(email=request.user.email)
            user_instance.facebook_access_token = new_token
            user_instance.facebook_user_id = fb_user_id
            user_instance.facebook_page_id = fb_page_id
            user_instance.instagram_user_id = ig_user_id
            print('here1')
            user_instance.save()
            print('here2')
            messages.success(request, f"Access token updated")
            return redirect(facebook_login)
        except:
            messages.error(request, f"Somethin goes wrong")
            return redirect(facebook_login)
    elif request.method == 'GET':
        return redirect(facebook_login)


@login_required(login_url='/login')
def instagram_create_post(request):
    if request.method == 'POST':
        user_instance = CustomUser.objects.get(email=request.user.email)
        woocommerce_id = request.POST.get("ig-selected-item", None)
        is_carousel = request.POST.get("is_carousel", None)
        caption = request.POST.get("caption", None)
        use_woocommerce_description = request.POST.get("use_woocommerce_description", None)
        print(use_woocommerce_description)
        print(woocommerce_id)
        print(is_carousel)
        print(caption)
        #woocommerce_product = woocommerce_retrieve_product_by_id(woocommerce_id)
        if is_carousel != None:
            print("make carousel")
            #image_urls = woocommerce_get_first_10_images(woocommerce_product)
            print(image_urls)
            ids_list = []
            ids_array = ''
            for url in image_urls:
                #id_media_container = instagram_create_container_media(user_instance, url, caption, True)                
                ids_array = '%2C'
                ids_list.append(id_media_container)

            for id_container in ids_list:
                print("instagram_check_container_validity(user_instance, id_container)")
            ids_array = ids_array[:-3]
            print(ids_array)

            if use_woocommerce_description != None:
                #item = retrieveItemBySku(woocommerce_product['sku'])
                print('NEW CAPTION')
                print(item.descriptionCustom)
                caption = item.descriptionCustom
            #carousel_id = instagram_create_container_carousel(user_instance, ids_array, caption)
            # pubblica container carosello
            #instagram_publish_carousel(user_instance, carousel_id)

        else:
            #make single media post
            print("make single media post")
            #instagram_create_container_media(user, url_image, caption, False)
        
        #instagram_create_container_media(user_instance,'https://xzshop.eu/wp-content/uploads/2023/02/61147517-3ead-4574-a7d0-bad816dba54b-1.jpg')
        return redirect(social_instagram)