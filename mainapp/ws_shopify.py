
from mainapp.ws_shopify_utils import ShopifyUtils
import shopify
import json
import requests
from ast import literal_eval
import re


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

    '''
    def shopify_creatroduct(item, variants):
        # Create a new product
        session = shopify.Session("https://sellfast-development-store.myshopify.com/", "2023-01", "")
        shopify.ShopifyResource.activate_session(session)
        new_product = shopify.Product()
        new_product.title = item.itemName
        new_product.body_html = item.descriptionTemplate

        image_set = ShopifyUtils.shopify_set_images(literal_eval(item.productImageSet))
        options_set = ShopifyUtils.shopify_set_options(item.attributes, variants)
        variants_set = ShopifyUtils.shopify_set_variants(options_set, variants)
        #print(variants_set)
        new_product.images = image_set
        #new_product.options = options_set
        #new_product.variants = variants_set
        #new_product.variants.attributes = {}
        #new_product.product_type = "Snowboard"
        #new_product.vendor = "Burton"
        print(new_product)
        success = new_product.save() #returns false if the record is invalid
        print(success)
        # or
        if new_product.errors:
            print(new_product.errors.full_messages())'''

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
