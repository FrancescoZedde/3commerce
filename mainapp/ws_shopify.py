
from mainapp.ws_shopify_utils import ShopifyUtils
import shopify
import json
import requests
from ast import literal_eval
import re



def shopify_exchange_code(shop, code):

    print('exchange code...')
    url = "https://" + shop + "/admin/oauth/access_token"
    payload = {
            'client_id': '700418a025a1df4a02784f0ed03362da',
            'client_secret': '264a8fc49e40cbfe57f2ce39da0e9cc5',
            'code': code,
            }

    response = requests.post(url, data=payload)

    print(response.json())

    return response.json()

class ShopifyConnect:
    def __init__(self, shopify_host, shopify_secret_key):
        try:
            session = shopify.Session(shopify_host, "2023-01", shopify_secret_key)
            shopify.ShopifyResource.activate_session(session)
            shop = shopify.Shop.current()
            self.status = 'valid'
        except:
            self.status = 'invalid'

class Shopify:
    def __init__(self, user):
        #start session
        #self.shopify = shopify.Session.setup(api_key="", secret="")
        self.api_key = user.shopify_secret_key
        self.host = user.shopify_host
        #print(self.shopify)

    def shopify_check_status():
        session = shopify.Session("https://sellfast-development-store.myshopify.com/", "2023-01", "")
        shopify.ShopifyResource.activate_session(session)
        shop = shopify.Shop.current()
        print(shop)

    def shopify_create_new_product(self, item, variants):

        image_set = ShopifyUtils.shopify_set_images(literal_eval(item.productImageSet))
        options_set = ShopifyUtils.shopify_set_options(item.attributes, variants)
        variants_set = ShopifyUtils.shopify_set_variants(options_set, variants)


        url = self.host + '/admin/api/2023-01/products.json'

        headers = {'X-Shopify-Access-Token': self.api_key,
                    'Content-Type': 'application/json'}

        payload = {
                    "product": {
                        "title": item.itemName,
                        "body_html": item.descriptionTemplate,
                        "product_type": "type test",
                        "vendor": "development-store",
                        "options" : options_set,
                        "variants": variants_set,
                        "images": image_set,
                        }
                    
                    }

        print(url)
        #print(payload)

        response = requests.post(url, json=payload, headers=headers).json()
        return response

    def shopify_add_images_to_variants(self, variants, create_product_response):

        shopify_variants_dict, images_names_shopify, images_names_sellfast = ShopifyUtils.shopify_match_skus_images_ids(variants, create_product_response)

        for sku, image_name in images_names_sellfast.items():
            id_shopify = shopify_variants_dict[sku]
            id_image = images_names_shopify[image_name]

            url = self.host + '/admin/api/2023-01/variants/' + str(id_shopify) +'.json'

            headers = {'X-Shopify-Access-Token': self.api_key,
                        'Content-Type': 'application/json'}

            data = {"variant": 
                {
                "id" : id_shopify,
                "image_id" : id_image,
                }
            }
            r = requests.put(url, data=json.dumps(data), headers=headers)


    def shopify_retrieve_all_products(self):
        url = self.host + '/admin/api/2023-01/products.json?limit=250'

        headers = {'X-Shopify-Access-Token': self.api_key,
                    'Content-Type': 'application/json'}

        response = requests.get(url, headers=headers).json()
        print('RETRIEVE ALL PRODUCT RESPONSE')
        print(response)



    def shopify_create_auth_url(self, shop_name):
        shop_url = shop_name + ".myshopify.com"
        api_version = '2023-01'
        state = "123456789"
        redirect_uri = "http://sellfast.app"
        scopes = ['read_products', 'read_orders']

        newSession = shopify.Session(shop_url, api_version)
        auth_url = newSession.create_permission_url(scopes, redirect_uri, state)

        return auth_url
