
from woocommerce import API
from users_app.models import CustomUser
from store_app.store_woocommerce_utils import create_jsonWooCommerceAddVariants, set_attributes, woocommerce_set_attributes
from main_app.db_functions import updateWoocommerceId_sku_filter, retrieveItemBySku, retrieveVariantsByItem, retrieve_item_by_user_and_sku
from ast import literal_eval
import json
import time

#Authentication

class WooCommerceConnect:
    def __init__(self, woocommerce_host, woocommerce_consumer_key, woocommerce_secret_key):
        self.wcapi = API(url= woocommerce_host,
                        consumer_key= woocommerce_consumer_key,
                        consumer_secret= woocommerce_secret_key,
                        wp_api=True,version="wc/v3",
                        timeout = 6000,)
        #test connection
        try:
            self.wcapi.get("products").json()
            self.status = 'valid'
        except:
            self.status = 'invalid'

class WooCommerce():
    def __init__(self, user):
        self.user = user
        self.wcapi = API(url= user.woocommerce_host,
                        consumer_key= user.woocommerce_consumer_key,
                        consumer_secret= user.woocommerce_secret_key,
                        wp_api=True,
                        version="wc/v3",
                        timeout = 6000,)
    
    def start_woocommerce_products_batch(self, sku_list, categories):
        products_batch_list = []
        for sku in sku_list:
            item = retrieve_item_by_user_and_sku(self.user, sku)


            json_woocommerce_export = create_json_products_batch(item, categories)
            item.jsonWooCommerceExport = str(json_woocommerce_export)
            item.save()
            products_batch_list.append(json_woocommerce_export)

            #response = self.wcapi.post("products", json_woocommerce_export).json()
            #print('response single product')
            #print(response)

        payload = {"create": products_batch_list}
        print('PAYLOAD BATCH PRODUCTS')
        #print(payload)
        response = self.wcapi.post("products/batch", payload).json()
        print(response)
        products_list = response['create']

        for woocommerce_item in products_list:
            
            woocommerce_product_images = woocommerce_item['images']
            images_dict_list = []
            for woocommerce_image in woocommerce_product_images:
                image_name = woocommerce_image['src'][woocommerce_image['src'].rindex('/')+1:]
                images_dict_list.append({image_name : woocommerce_image['id']})

            print('images_dict_list')
            print(images_dict_list)

            woocommerce_product = self.woocommerce_get_product_by_id(woocommerce_item['id'])
            product_sku = woocommerce_product['sku']
            print(product_sku)
            inventory_item = updateWoocommerceId_sku_filter(self.user, product_sku, woocommerce_item['id'] )

            variants = retrieveVariantsByItem(inventory_item)

            jsonwoocommercevariants = create_json_variants_batch(woocommerce_item, variants, images_dict_list)

            endpoint = "products/"+str(woocommerce_item['id'])+"/variations/batch"

            response = self.wcapi.post(endpoint, jsonwoocommercevariants).json()

            #print(response)
    

    def woocommerce_get_product_by_id(self, wocommerce_id):
        endpoint = "products/" + str(wocommerce_id)
        response = self.wcapi.get(endpoint).json()
        print(response)
        return response

    def woocommerce_retrieve_all_products(self):
        products_list = []
        for i in range(1,10):
            try:
                endpoint = "products"
                params = {  'page': str(i),
                            'per_page': '100',
                        }
                response = self.wcapi.get(endpoint, params=params).json()
                print(response)
                products_list = products_list + response
                print(len(products_list))
                if len(response) < 100:
                    break
            except:
                break
        
        return products_list
    
    def woocommerce_retrieve_limited_products(self):
        products_list = []
        endpoint = "products"
        params = {  'page': 1,
                    'per_page': '25',
                  }
        products_list = self.wcapi.get(endpoint, params=params).json()
        print(products_list)
        return products_list

    def woocommerce_retrieve_product_variations(self, woocommerce_id):
        endpoint = "products/" + str(woocommerce_id) + "/variations"
        response = self.wcapi.get("products/794").json()
        print(response)

    def woocommerce_update_variation_description(self, product_woocommerce_id, variation_woocommerce_id, new_description):
        #wcapi.put("products/22/variations/733", data).json()
        endpoint = "products/" + str(product_woocommerce_id) + "/variations/" + str(variation_woocommerce_id)
        data = {
                "description": str(new_description)
                }
        response = self.wcapi.put("products/794", data).json()
        print(response)

    def woocommerce_update_description(self, woocommerce_id, new_description):
        endpoint = "products/" + str(woocommerce_id)
        data = {
                "description": str(new_description)
                }
        response = self.wcapi.put(endpoint, data).json()
        print(response)
  

    def woocommerce_delete_product(self, woocommerce_id, force):

        endpoint = "products/" + str(woocommerce_id)
        params = {"force": force}


        response = self.wcapi.delete(endpoint, params=params).json()
        print('product delete')
        print(params)
        print(response)
        return response

    def get_woocommerce_categories(self):
        params = {'per_page': '99'}
        woocommerce_categories = self.wcapi.get("products/categories", params=params).json()

        return woocommerce_categories

    def woocommerce_retrieve_all_orders(self):
        orders = self.wcapi.get("orders").json()
        return orders



def create_woocommerce_category(name, slug):
    wcapi = woocommerce_authentication()
    data = {
        "name": name,
        "slug" : create_woocommerce_category,

    }
    response = wcapi.post("products/categories", data).json()
    print(response)
    return response


def get_woocommerce_categories():
    wcapi = woocommerce_authentication()
    params = {'per_page': '99'}
    woocommerce_categories = wcapi.get("products/categories", params=params).json()

    return woocommerce_categories


def create_json_products_batch(item, categories):
    img_set = set_img_set(item)
    #woocommerce_categories = get_woocommerce_categories()
    attrbs, default_attributes = woocommerce_set_attributes(json.loads(item.jsonDataImported))
    #default_attributes = set_default_attributes()
    #product_categories = set_product_categories()
    category_set = []
    for category in categories:
        c = {'id': int(category)}
        category_set.append(c)

    #attrbs, default_attributes, product_categories = set_attributes(woocommerce_categories, product_details)
    
    #print(default_attributes)
    
    json_woocommerce_export = {
        "name": item.itemName,
        "type": "variable",
        "categories": category_set,
        'stock_status':'instock',
        'stock_quantity': 255,
        "description": item.descriptionTemplate,
        "short_description":'' ,
        "price" : item.sellPrice,
        "sku": item.sku,
        "images": img_set,
        "attributes": attrbs,
        "default_attributes": default_attributes
        }
    
    print(json_woocommerce_export)

    return json_woocommerce_export

def create_json_variants_batch(item, variants, images_dict_list):
    attributes_names = item['attributes']
    print('attributesxxx')
    print(attributes_names)
    #attributes_names = attributes_names.split("-")
    print(images_dict_list)
    variants_list = []
    for variant in variants:

        #match image
        img_name_key = variant.variantImage[variant.variantImage.rindex('/')+1:]
        print('match image ...')
        
        print(img_name_key)
        for images_dict in images_dict_list:
            if img_name_key in images_dict:
                print('id matched')
                image_id = images_dict.get(img_name_key)
                print(image_id)
            '''
            try:
                image_id = images_dict.get(img_name_key)
            except:
                pass'''



        attributes = []
        variant_values = variant.variantKey
        variant_values = variant_values.split("-")
        print(variant_values)
        for i in range(len(variant_values)):
            single_attribute = { "name": attributes_names[i]['name'], "option": variant_values[i]}
            attributes.append(single_attribute)
        
        variant_data = { "regular_price": variant.sellPrice,
                 "sku": variant.variantSku,
                 "attributes":attributes,
                 "image": {
                    "id" : str(image_id),
                    }
               }
        variants_list.append(variant_data)

    jsonwoocommercevariants = {"create": variants_list}
    print('jsonwoocommercevariants')
    print(jsonwoocommercevariants)
    #variant.jsonWooCommerceExportVariants = str(jsonwoocommercevariants)

    #variant.save()

    return jsonwoocommercevariants

def set_img_set(item):

    img_set = []
    for image in literal_eval(item.productImageSet):
        img = {"src": image}
        img_set.append(img)

    variants = retrieveVariantsByItem(item)
    for variant in variants:
        img_set.append({"src": str(variant.variantImage)})
    
    print('IMG SET')
    print(img_set)
    return img_set


def retrieve_woocommerce_attributes():
    wcapi = woocommerce_authentication()

    response = wcapi.get("products/attributes").json()

    attributes = []

    for attribute in response:
        attributes.append(attribute['slug'])

    #attributes is a list of all woocomm attributes, take values from slug
    return attributes



def create_woocommerce_attribute(product_or_variant_attribute):
    wcapi = woocommerce_authentication()

    data = {
            "name": product_or_variant_attribute.capitalize(),
            "slug": product_or_variant_attribute,
            "type": "select",
            "order_by": "menu_order",
            "has_archives": True
            }

    response = wcapi.post("products/attributes", data).json()
    print(response)
    return response




def woocommerce_retrieve_product_by_id(woocommerce_id):
    wcapi = woocommerce_authentication()
    endpoint = 'products/' + str(woocommerce_id)
    response = wcapi.get(endpoint).json()
    print(response)
    return response