from mainapp.ws_ebay_utils import base64_encode_credentials


import requests
import json
import base64
import urllib
'''
The client credentials grant flow

Get Application acces token. Scopes:

https://api.ebay.com/oauth/api_scope -> View public data from eBay

Sandbox	POST https://api.sandbox.ebay.com/identity/v1/oauth2/token
Production	POST https://api.ebay.com/identity/v1/oauth2/token
'''
def refresh_access_token():
    
    client_id = 'xzshop-d-PRD-a7db68d0a-cf529eb1' 
    client_secret = 'PRD-7db68d0a4bf9-5af1-4426-b52a-5044'
    rt = 'v^1.1#i^1#f^0#I^3#r^1#p^3#t^Ul41Xzk6NTc4NjIyMjY4NDc5NjZGQ0QwQUI5NzJBNTY1QTI3ODhfMV8xI0VeMjYw'

    url = 'https://api.ebay.com/identity/v1/oauth2/token'
    
    basic_auth = base64_encode_credentials(client_id, client_secret)
    headers = {"Content-Type": 'application/x-www-form-urlencoded',
              'Authorization': basic_auth}
    
    #url_encoded_scopes = 
    payload = {'grant_type' : 'refresh_token',
               'refresh_token': rt,
           'scope': 'https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.inventory' ,
          }
    data = urllib.parse.urlencode(payload)
    response = requests.post(url, data=data, headers=headers).json()
    print(response)
    return response['access_token']


def get_application_access_token(client_id, client_secret):
    #client_id = 'xzshop-d-PRD-a7db68d0a-cf529eb1'
    #client_secret = 'PRD-7db68d0a4bf9-5af1-4426-b52a-5044'
    url = 'https://api.ebay.com/identity/v1/oauth2/token'
    basic_auth = base64_encode_credentials(client_id, client_secret)
    headers = {"Content-Type": 'application/x-www-form-urlencoded',
              'Authorization': basic_auth}
    
    #url_encoded_scopes = 
    payload = {'grant_type' : 'client_credentials',
           'scope': 'https://api.ebay.com/oauth/api_scope' ,
          }
    data = urllib.parse.urlencode(payload)

    response = requests.post(url, data=data, headers=headers).json()
    print(response)

    #get_application_access_token('xzshop-d-PRD-a7db68d0a-cf529eb1', 'PRD-7db68d0a4bf9-5af1-4426-b52a-5044')
'''
Sandbox POST https://api.sandbox.ebay.com/identity/v1/oauth2/token
Production  POST https://api.ebay.com/identity/v1/oauth2/token
'''

def get_all_inventory_items(access_token):
    #access_token = refresh_access_token()
    url = 'https://api.ebay.com/sell/inventory/v1/inventory_item?limit=100'
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(url, headers=headers).json()
    print(response)
    return response


def ebay_delete_inventory_item(sku, access_token):
    
    #access_token = refresh_access_token()
    url = 'https://api.ebay.com/sell/inventory/v1/inventory_item/' +  str(sku)

    print(url)
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.delete(url, headers=headers)
    print(response)


def ebay_create_inventory_location():
    access_token = refresh_access_token()
    url = 'https://api.ebay.com/sell/inventory/v1/location/' + 'test-location-cn-warehouse-1612'
    headers = {'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/json'}

    payload = {
                "location": {
                    "address": {
                        "addressLine1": "test",
                        "addressLine2": "test2",
                        "city": "Singapore",
                        "stateOrProvince": "SNP",
                        "postalCode": "96765",
                        "country": "CN"
                    }
                },
                "locationInstructions": "Items ship from here.",
                "name": "CHINA-WAREHOUSE-1",
                "merchantLocationStatus": "ENABLED",
                "locationTypes": [
                    "WAREHOUSE"
                ]
                }

    response = requests.post(url, json=payload, headers=headers)
    print(response)

def ebay_get_inventory_location():
    access_token = refresh_access_token()
    url = 'https://api.ebay.com/sell/inventory/v1/location'
    

    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(url, headers=headers).json()
    print(response)
'''
payload = {
    "title": "Test Group",
    "description": "Men's solid polo shirts in five colors (Green, Blue, Red, Black, and White), and sizes ranges from small to XL.",
    "variantSKUs": [
        "XZTESTSKU001",
        "XZTESTSKU000",
    ]
}
'''

def create_inventory_items_group(access_token, payload, inventory_item_group_key):
    #access_token = refresh_access_token()
    url = 'https://api.ebay.com/sell/inventory/v1/inventory_item_group/' + str(inventory_item_group_key)
    headers = {'Authorization': 'Bearer ' + access_token,
              'Content-Type': 'application/json',
              "Content-Language": "en-US"}
    response = requests.put(url, json=payload, headers=headers)
    if response.status_code != 204:
        print(response.json())
    else:
        pass
    #return response


def create_inventory_item(access_token, payload):
    url = 'https://api.ebay.com/sell/inventory/v1/bulk_create_or_replace_inventory_item'
    headers = {'Authorization': 'Bearer ' + access_token,
              'Content-Type': 'application/json',
              "Content-Language": "en-US"}
    response = requests.post(url, json=payload, headers=headers).json()
    print(response)
    return response

def bulk_create_offer(access_token, payload):
    #access_token = refresh_access_token()
    url = 'https://api.ebay.com/sell/inventory/v1/bulk_create_offer'
    headers = {'Authorization': 'Bearer ' + access_token,
              'Content-Type': 'application/json',
              "Content-Language": "en-US"}
    response = requests.post(url, json=payload, headers=headers).json()
    print('bulk_create_offer response')
    print(response)
    return response['responses']

def ebay_bulk_publish_offer(payload):
    access_token = refresh_access_token()
    print(payload)
    url = 'https://api.ebay.com/sell/inventory/v1/bulk_publish_offer'
    headers = {'Authorization': 'Bearer ' + access_token,
              'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers).json()
    print('ebay_bulk_publish_offer response')
    print(response)

def ebay_publish_offer(access_token, offerId):
    #access_token = refresh_access_token()
    url = 'https://api.ebay.com/sell/inventory/v1/offer/' +str(offerId) +'/publish/'
    print(url)
    headers = {'Authorization': 'Bearer ' + access_token,
              'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers).json()
    print('EBAY PUBLISH SINGLE OFFER RESPONSE')
    print(response)

def ebay_publish_by_inventory_item_group(access_token, item_group_key):
    url = 'https://api.ebay.com/sell/inventory/v1/offer/publish_by_inventory_item_group'
    payload = {
        "inventoryItemGroupKey" : str(item_group_key),
        "marketplaceId" : "EBAY_US"
    }
    headers = {'Authorization': 'Bearer ' + access_token,
              'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers).json()

    print(response)
    return response

def ebay_search_items_by_keywords(access_token, keywords):
    url = 'https://api.ebay.com/buy/browse/v1/item_summary/search'
    params = {
        'q': keywords,
        'limit': '5',
    }
    headers = {'Authorization': 'Bearer ' + access_token,
              'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['itemSummaries']
    else:
        return response.status_code



'''
GET https://api.ebay.com/commerce/catalog/v1_beta/product_summary/search?
q=string&
gtin=string&
mpn=string&
category_ids=string&
aspect_filter=AspectFilter&
fieldgroups=string&
limit=string&
offset=string&
'''
def ebay_match_product_with_ebay_catalog(access_token, keywords, gtin):
    url = 'https://api.ebay.com/commerce/catalog/v1_beta/product_summary/search'
    params = {
        'q': keywords,
        'gtin': gtin,
    }
    headers = {'Authorization': 'Bearer ' + access_token,
              'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers, params=params)
    print(response)
    print(response.json())




#bulk_create_offer


