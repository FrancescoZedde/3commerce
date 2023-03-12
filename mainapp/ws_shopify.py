#client id 6fb5b0131320a2eb79762a37c255b9aa
# secret d89906da5b9641cab0d92edb7472a3d4



# App created from Admin store 
# clinet id 669bba2f5b16fe9f02d41053b120c756
#client secret 15e0e09582aca11f950bd8cbaccf0c80
# access token generate dfrom admin app : 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
from mainapp.ws_shopify_utils import ShopifyUtils
import shopify
import json
import requests
from ast import literal_eval

class Shopify:
    def __init__(self):
        #start session
        self.shopify = shopify.Session.setup(api_key="6fb5b0131320a2eb79762a37c255b9aa", secret="d89906da5b9641cab0d92edb7472a3d4")
        print(self.shopify)

    def shopify_check_status():
        session = shopify.Session("https://sellfast-development-store.myshopify.com/", "2023-01", "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")
        shopify.ShopifyResource.activate_session(session)
        shop = shopify.Shop.current()
        print(shop)

    def shopify_create_new_product(item, variants):
        # Create a new product
        session = shopify.Session("https://sellfast-development-store.myshopify.com/", "2023-01", "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")
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
            print(new_product.errors.full_messages())

    def shopify_create_new_product_test(item, variants):

        image_set = ShopifyUtils.shopify_set_images(literal_eval(item.productImageSet))
        options_set = ShopifyUtils.shopify_set_options(item.attributes, variants)
        variants_set = ShopifyUtils.shopify_set_variants(options_set, variants)


        url = 'https://sellfast-development-store.myshopify.com/' + 'admin/api/2023-01/products.json'

        headers = {'X-Shopify-Access-Token': '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',
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

        print(payload)

        response = requests.post(url, json=payload, headers=headers).json()
        #print(response)

    def shopify_create_auth_url(self, shop_name):
        shop_url = shop_name + ".myshopify.com"
        api_version = '2020-10'
        state = "123456789"
        redirect_uri = "http://redirect.xzshop.eu"
        scopes = ['read_products', 'read_orders']

        newSession = self.shopify.Session(shop_url, api_version)
        auth_url = newSession.create_permission_url(scopes, redirect_uri, state)

        return auth_url
