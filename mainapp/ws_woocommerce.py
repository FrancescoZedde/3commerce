
from woocommerce import API
from users.models import CustomUser
from mainapp.ws_woocommerce_utils import create_jsonWooCommerceAddVariants, set_attributes, woocommerce_set_attributes
from mainapp.db_functions import updateWoocommerceId_sku_filter, retrieveItemBySku, retrieveVariantsByItem
from mainapp.db_functions import retrieve_item_by_user_and_sku
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
                        wp_api=True,version="wc/v3",
                        timeout = 6000,)
    
    def start_woocommerce_products_batch(self, sku_list, categories):
        products_batch_list = []
        for sku in sku_list:
            item = retrieve_item_by_user_and_sku(self.user, sku)
            json_woocommerce_export = create_json_products_batch(item, categories)
            item.jsonWooCommerceExport = str(json_woocommerce_export)
            item.save()
            products_batch_list.append(json_woocommerce_export)

        payload = {"create": products_batch_list}
        response = self.wcapi.post("products/batch", payload).json()
        print(response)
        products_list = response['create']

        for woocommerce_item in products_list:
            woocommerce_product = self.woocommerce_get_product_by_id(woocommerce_item['id'])
            product_sku = woocommerce_product['sku']
            print(product_sku)
            inventory_item = updateWoocommerceId_sku_filter(self.user, product_sku, woocommerce_item['id'] )

            variants = retrieveVariantsByItem(inventory_item)

            jsonwoocommercevariants = create_json_variants_batch(woocommerce_item, variants)

            endpoint = "products/"+str(woocommerce_item['id'])+"/variations/batch"

            response = self.wcapi.post(endpoint, jsonwoocommercevariants).json()

            print(response)
    

    def woocommerce_get_product_by_id(self, wocommerce_id):
        endpoint = "products/" + str(wocommerce_id)
        response = self.wcapi.get(endpoint).json()
        print(response)
        return response

    def woocommerce_retrieve_all_products(self):
        endpoint = "products"
        params = {'per_page': '99',
                  }
        response = self.wcapi.get(endpoint, params=params).json()
        return response
    
    def get_woocommerce_categories(self):
        params = {'per_page': '99'}
        woocommerce_categories = self.wcapi.get("products/categories", params=params).json()

        return woocommerce_categories





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


def start_woocommerce_products_batch(sku_list, categories):
    wcapi = woocommerce_authentication()
    products_batch_list = []
    for sku in sku_list:
        #retrieveItemBySku, retrieveVariantsByItem
        item = retrieveItemBySku(sku)
        print(item)
        #create json export woocommerce batch
        json_woocommerce_export = create_json_products_batch(item, categories)
        
        #save json
        item.jsonWooCommerceExport = str(json_woocommerce_export)
        item.save()

        #append to list of products
        products_batch_list.append(json_woocommerce_export)
        #response = wcapi.post("products", jsonWooCommerceExport).json()

    payload = {"create": products_batch_list}
    print(payload)

    # products batch call
    response = wcapi.post("products/batch", payload).json()
    print(response)
    #time.sleep(15)
    products_list = response['create']

    for woocommerce_item in products_list:
        print(woocommerce_item)
        #item = json.loads(item)
        woocommerce_product = get_woocommerce_product_by_id(woocommerce_item['id'])
        product_sku = woocommerce_product['sku']
        print(product_sku)
        inventory_item = updateWoocommerceId_sku_filter(product_sku,woocommerce_item['id'] )

        variants = retrieveVariantsByItem(inventory_item)

        jsonwoocommercevariants = create_json_variants_batch(woocommerce_item, variants)

        endpoint = "products/"+str(woocommerce_item['id'])+"/variations/batch"

        response = wcapi.post(endpoint, jsonwoocommercevariants).json()
    
        print(response)  

        #update inventoryItem woocommerceId

        #for each item retireve variants and create json variants batch

        #make call to export variants
        #jsonWooCommerceExportVariants = create_json_variants_batch(item, variants)


def create_json_products_batch(item, categories):
    img_set = set_img_set(literal_eval(item.productImageSet))
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

def create_json_variants_batch(item, variants):
    attributes_names = item['attributes']
    print('attributesxxx')
    print(attributes_names)
    #attributes_names = attributes_names.split("-")
    
    variants_list = []
    for variant in variants:
        attributes = []
        variant_values = variant.variantKey
        variant_values = variant_values.split("-")
        print(variant_values)
        for i in range(len(variant_values)):
            single_attribute = { "name": attributes_names[i]['name'], "option": variant_values[i]}
            attributes.append(single_attribute)
        
        variant_data = { "regular_price": variant.sellPrice,
                 "sku": variant.variantSku,
                 "attributes":attributes
               }
        variants_list.append(variant_data)
    
    jsonwoocommercevariants = {"create": variants_list}
    print('jsonwoocommercevariants')
    print(jsonwoocommercevariants)
    #variant.jsonWooCommerceExportVariants = str(jsonwoocommercevariants)

    #variant.save()

    return jsonwoocommercevariants

def set_img_set(productImageSet):
    img_set = []
    for image in productImageSet:
        img = {'src': image}
        img_set.append(img)
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