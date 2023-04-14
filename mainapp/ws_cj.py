from django.conf import settings
import requests
import json
import math

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
    
    return resp['data']

def cj_get_inventory_inquiry(vid):
    access_token = cj_authentication()

    url = "https://developers.cjdropshipping.com/api2.0/v1/product/stock/queryByVid?vid=" + str(vid)

    headers = {"CJ-Access-Token": access_token}

    response = requests.get(url, headers=headers).json()

    print(response)
    
    return response['data']