from django.conf import settings
import requests
import json
import math
from mainapp.models import Variant

#from mainapp.ws_woocommerce import create_woocommerce_category

# CJ dropshipping 
# get access token


class CJDropshippingConnect():
    def __init__(self, cj_email, cj_key):
        try:
            url = 'https://developers.cjdropshipping.com/api2.0/v1/authentication/getAccessToken'
            data = {"email": cj_email,
                    "password": cj_key}
            auth_resp = requests.post(url, json = data).json()
            access_token = auth_resp['data']['accessToken']
            self.status = 'valid'
        except:
            self.status = 'invalid'


class CJDropshipping:
    def __init__(self, user):
        url = 'https://developers.cjdropshipping.com/api2.0/v1/authentication/getAccessToken'
        data = {"email": user.cjdropshipping_email,
                "password": user.cjdropshipping_api_key}
        auth_resp = requests.post(url, json = data).json()

        self.access_token = auth_resp['data']['accessToken']
    
    def cj_get_access_token(self):
        return self.access_token

    def cj_products_by_category(self, category_id, results_limit):
        url = 'https://developers.cjdropshipping.com/api2.0/v1/product/list'
        n_page = math.ceil(int(results_limit)/200)
        response = []
        for i in range(int(n_page)+1):
            try:
                if i != 0:
                    print(i)
                    data = {"pageNum": i,
                           "pageSize": '200',
                            'categoryId': category_id}
                    headers = {"CJ-Access-Token": self.access_token}

                    get_products_resp = requests.get(url, params=data, headers=headers).json()
                    lista_prodotti = get_products_resp['data']['list']
                    response = response + lista_prodotti
            except:
                break
        return response[0:int(results_limit)]
    
    def cj_get_product_details(self, sku):        
        url = 'https://developers.cjdropshipping.com/api2.0/v1/product/query?productSku=' + str(sku)
        headers = {"CJ-Access-Token": self.access_token}

        response = requests.get(url, headers=headers).json()

        #print(response)
        product_details = response['data']

        return product_details

    def cj_get_shipping_methods(self, vid, startCountryCode, endCountryCode):
        url = 'https://developers.cjdropshipping.com/api2.0/v1/logistic/freightCalculate'
        data = { 
            "startCountryCode": startCountryCode,
            "endCountryCode": endCountryCode,
            "products": [
                        {
                            "quantity": 1,
                            "vid": vid
                        }
                    ]
                }
        resp = requests.post(url, json = data).json()
        print(' SHIPPING METHODS: ')
        print(resp)

        return resp['data']


    def cj_create_order(self, order_object, products):
        url = 'https://developers.cjdropshipping.com/api2.0/v1/shopping/order/createOrder'

        print(products)
        
        products_list = []
        for product in products:
            variant = Variant.objects.filter(variantSku=product['sku'])
            products_list.append({"vid": variant[0].vid , "quantity": int(product['quantity']), "shippingName": product['name']})

        headers = {"CJ-Access-Token": self.access_token,
                    "Content-Type": "application/json"}
        data = {
                    "shippingZip": order_object.shipping_zip,
                    "shippingCountryCode": order_object.shipping_country_code,
                    "shippingCountry": order_object.shipping_country,
                    "shippingProvince": order_object.shipping_province,
                    "shippingCity": order_object.shipping_city,
                    "shippingAddress": order_object.shipping_address,
                    "shippingCustomerName": order_object.shipping_customer_name,
                    "shippingPhone": order_object.shipping_phone,
                    "remark": order_object.remark,
                    "fromCountryCode": "CN",
                    "logisticName": order_object.logistic_name,
                    "products": products_list
                }
        order = requests.post(url, json = data, headers=headers).json()
        print(' orderS: ')
        print(order)

        return order['data']

    
    def cj_get_track_info(track_number):
        url = f'https://developers.cjdropshipping.com/api2.0/v1/logistic/getTrackInfo?trackNumber={track_number}'
        response = requests.get(url)
        return response.json()
'''

'''



'''
def cj_authentication():
    url = 'https://developers.cjdropshipping.com/api2.0/v1/authentication/getAccessToken'
    data = {"email": settings.CJ_EMAIL,
            "password": settings.CJ_PWD}
    auth_resp = requests.post(url, json = data).json()
    access_token = auth_resp['data']['accessToken']

    return access_token


# get products by category id
def cj_products_by_category(category_id, results_limit):
    access_token = cj_authentication()
    url = 'https://developers.cjdropshipping.com/api2.0/v1/product/list'

    n_page = math.ceil(int(results_limit)/200)
    print(n_page)

    response = []
    for i in range(int(n_page)+1):
        try:
            if i != 0:
                print(i)
                data = {"pageNum": i,
                       "pageSize": '200',
                        'categoryId': category_id}
                headers = {"CJ-Access-Token": access_token}

                get_products_resp = requests.get(url, params=data, headers=headers).json()
                lista_prodotti = get_products_resp['data']['list']
                response = response + lista_prodotti
        except:
            break
    return response[0:int(results_limit)]


def cj_get_product_details(sku):
    access_token = cj_authentication()
    
    url = 'https://developers.cjdropshipping.com/api2.0/v1/product/query?productSku=' + str(sku)
    headers = {"CJ-Access-Token": access_token}

    response = requests.get(url, headers=headers).json()

    #print(response)
    product_details = response['data']

    return product_details

def cj_get_shipping_methods(vid, startCountryCode, endCountryCode):
    url = 'https://developers.cjdropshipping.com/api2.0/v1/logistic/freightCalculate'
    data = { 
        "startCountryCode": startCountryCode,
        "endCountryCode": endCountryCode,
        "products": [
                    {
                        "quantity": 1,
                        "vid": vid
                    }
                ]
            }
    resp = requests.post(url, json = data).json()
    print(' SHIPPING METHODS: ')
    print(resp)
    
    return resp['data']'''

def cj_get_inventory_inquiry(vid):
    access_token = cj_authentication()

    url = "https://developers.cjdropshipping.com/api2.0/v1/product/stock/queryByVid?vid=" + str(vid)

    headers = {"CJ-Access-Token": access_token}

    response = requests.get(url, headers=headers).json()

    print(response)
    
    return response['data']