import pandas as pd
import re
import json
from mainapp.models import InventoryItem, Variant, WoocommerceStore
from users.models import CustomUser
from ast import literal_eval
import html
import math
from bs4 import BeautifulSoup




def connect_woocommerce_store(user, store_name, host, ck, cs):
    user.store_type = 'woocommerce'
    user.store_name = store_name
    user.woocommerce_store_name = store_name
    user.woocommerce_host = host = host
    user.woocommerce_consumer_key = ck
    user.woocommerce_secret_key = cs
    user.save()

def reset_woocommerce_store(user):
    user.store_type = 'none'
    user.store_name = ''
    user.woocommerce_store_name = ''
    user.woocommerce_host = host = ''
    user.woocommerce_consumer_key = ''
    user.woocommerce_secret_key = ''
    user.save()

def reset_cjdropshipping(user):
    user.cjdropshipping_api_key = ''
    user.cjdropshipping_email = ''
    user.save()

def connect_shopify_store(user, store_name, host, ck, cs):
    user.store_type = 'shopify'
    user.store_name = store_name
    user.shopify_store_name = store_name
    user.shopify_host = host = host
    user.shopify_consumer_key = ck
    user.shopify_secret_key = cs
    user.save()

def connect_cj_account(user, cj_email, cj_key):
    user.cjdropshipping_email = cj_email
    user.cjdropshipping_api_key = cj_key
    user.save()

def reset_shopify_store(user):
    user.store_type = 'none'
    user.store_name = ''
    user.shopify_store_name = ''
    user.shopify_host = host = ''
    user.shopify_consumer_key = ''
    user.shopify_secret_key = ''
    user.save()

def update_woocommerce_on_sale_status(sku):
    item = InventoryItem.objects.get(sku=sku)
    if item.onsaleWoocommerce == True:
        item.onsaleWoocommerce == False
        item.save()
    else:
        item.onsaleWoocommerce == True
        item.save()

def update_ebay_on_sale_status(sku):
    item = InventoryItem.objects.get(sku=sku)
    if item.onsaleEbay == True:
        item.onsaleEbay == False
        item.save()
    else:
        item.onsaleEbay == True
        item.save()


def retrieveAllInventoryItems():
    all_inventory_items = InventoryItem.objects.all().order_by('-id')
    return all_inventory_items

def retrieveInventoryItemById(pk):
    obj = InventoryItem.objects.get(id=pk)
    return obj

def retrieveItemBySku(sku):
    item = InventoryItem.objects.get(sku=sku)
    return item

def retrieve_item_by_user_and_sku(user, sku):
    item = InventoryItem.objects.filter(user=user, sku=sku)
    return item[0]

def retrieveVariantBySku(sku):
    print(sku)
    variant = Variant.objects.get(variantSku=sku)
    return variant

def retrieveVariantsByItem(item):
    variants = Variant.objects.filter(item=item) 
    return variants

def retrieveitemByWoocommerceId(woocommerce_id):
    item = InventoryItem.objects.get(woocommerceId=woocommerce_id)
    return item

def updateWoocommerceId_sku_filter(user, sku, woocommerceId):
    item = InventoryItem.objects.filter(user=user, sku=sku)
    item[0].woocommerceId = woocommerceId
    item[0].save()
    return item[0]

def deleteItemBySku(user, sku):
    item = InventoryItem.objects.filter(user=user, sku=sku)
    try:
        item.delete()
        message = 'Item(s) deleted'
    except:
        message = 'Errore trying to delete item ' + str(sku)
    return message

def create_item_and_variants(product_details, user):
    categories_dict = parse_cj_categories(product_details)
    print('create_item_and_variants')
    inventory_item = InventoryItem( user = user,
                                    sku = product_details['productSku'],
                                    itemName = product_details['productNameEn'],
                                    description = product_details['description'],
                                    supplierSellPrice = product_details['sellPrice'],
                                    sellPrice = float(0.00),
                                    supplier = 'CJ',
                                    supplierSku = product_details['productSku'],
                                    categoryFirst = categories_dict['first'],
                                    categorySecond = categories_dict['second'],
                                    categoryThird = categories_dict['third'],
                                    categoryFourth = '',
                                    attributes = product_details['productKeyEn'].lower(),
                                    productWeight =  product_details['productWeight'],
                                    productType =  product_details['productType'],
                                    entryNameEn = product_details['entryNameEn'],
                                    materialNameEn = product_details['materialNameEn'],
                                    packingWeight = product_details['packingWeight'],
                                    productImage = str(literal_eval(product_details['productImage'])[0]),
                                    productImageSet =product_details['productImageSet'],
                                    jsonVariants = json.dumps(product_details['variants']),
                                    jsonDataImported = json.dumps(product_details),
                                    jsonWooCommerceExport = '',
                                    jsonWooCommerceExportVariants = '',
                                    jsonEbayExportCreateInventoryItems = '',
                                    jsonEbayExportCreateItemsGroup = '',
                                    jsonEbayExportCreateOffers = '',)
    inventory_item.save()

    
    variants = product_details['variants']
    for variant in variants:
        print('create_variant')
        create_variant(inventory_item, variant)
    return inventory_item
    

def create_variant(inventory_item, variant):
    variant = Variant(item = inventory_item,
                                        vid = variant['vid'],
                                        variantSku = variant['variantSku'],
                                        variantNameEn = str(variant['variantNameEn']),
                                        description = 'variant description',
                                        supplierSellPrice = variant['variantSellPrice'],
                                        sellPrice = float(0.00),
                                        supplier = 'CJ',
                                        supplierSku = variant['variantSku'],
                                        variantImage= variant['variantImage'],
                                        variantKey= variant['variantKey'],
                                        variantLength= variant['variantLength'],
                                        variantWidth= variant['variantWidth'],
                                        variantHeight= variant['variantHeight'],
                                        variantVolume= variant['variantVolume'],
                                        variantWeight= variant['variantWeight'],
                                        firstShippingMethod = '',
                                        secondShippingMethod = '',
                                        thirdShippingMethod = '',
                                        #allShippingMethods  = shipping_methods_list,
                                        )

    variant.save()

def update_items_offer(user, selected_items, percentage_increase, minimumprice, roundat, use_preset_price):
    for sku in selected_items:
        print(sku)
        item_object = retrieve_item_by_user_and_sku(user, sku)
        print(item_object)
        updated_item = set_item_price(item_object, percentage_increase, minimumprice, roundat, use_preset_price)        
        #updated_item.selectcategories = select_categories
        updated_item.save()

        variants_query_set = Variant.objects.filter(item=updated_item) 
        for variant in variants_query_set:
            #da aggiungere categorie + shipping options
            variant = set_variant_price(variant, percentage_increase, minimumprice, roundat, use_preset_price)
            variant.save()
            

def update_item(data):
    sku = data.split("&", 1)[0]
    updates_dict = string_to_dict(data)
    enc = bytes(updates_dict['description'], 'utf-8')
    decodedLine = enc.decode('utf-8')
    item_object_set = InventoryItem.objects.filter(sku=sku)
    item_object =item_object_set[0]
    item_object.itemName = updates_dict['itemName']
    #item_object.description = decodedLine
    item_object.sellPrice = float(updates_dict['sellPrice'])
    item_object.attributes = updates_dict['attributes'].lower()

    item_object.save()

    return updates_dict

def update_variant(data):
    sku = data.split("&", 1)[0]
    print(sku)
    updates_dict = string_to_dict(data)
    variant_object_set = Variant.objects.filter(variantSku=sku)
    variant_object = variant_object_set[0]
    variant_object.variantNameEn = updates_dict['variantNameEn']
    #item_object.description = decodedLine
    variant_object.sellPrice = float(updates_dict['sellPrice'])
    variant_object.variantKey = updates_dict['variantKey'].lower()

    variant_object.save()

def string_to_dict(string):
    updates = string.split("&", 1)[1]
    updates = updates.split("&")
    updates_dict = {}
    for update in updates:
        update = update.replace('+', ' ')
        try:
            values = update.split('=',1)
            updates_dict[values[0]] = values[1]
        except:
            pass
    return updates_dict


def set_item_price(item_object, percentage_increase, minimumprice, roundat, use_preset_price):
    if '-' in item_object.supplierSellPrice or '--' in item_object.supplierSellPrice:
        if '-' in item_object.supplierSellPrice:
            min_and_max = item_object.supplierSellPrice.split("-")
        elif '--' in item_object.supplierSellPrice:
            min_and_max = item_object.supplierSellPrice.split("--")
        print(min_and_max)
        print(use_preset_price)
        if use_preset_price == 'on' or use_preset_price == True:
            min_price = float(min_and_max[0])
            max_price = float(min_and_max[1])
        else:
            min_price = float(min_and_max[0]) + float(min_and_max[0]) * ( float(percentage_increase)/float(100) )
            max_price = float(min_and_max[1]) + float(min_and_max[1]) * ( float(percentage_increase)/float(100) )

        # set minimumprice as minimum is the min_price is <
        if float(min_price) < float(minimumprice):
            min_price = float(minimumprice)
            if max_price < min_price:
                max_price = min_price*1.2

        #round prices
        min_price = math.modf(min_price)[1] + float(roundat)
        max_price = math.modf(max_price)[1] + float(roundat)


        item_object.sellPrice = str(min_price) + '-' + str(max_price)

        return item_object
    else:
        supplier_price = float(item_object.supplierSellPrice)

        if use_preset_price == 'on' or use_preset_price == True:
            sell_price = supplier_price
        else:
            sell_price = supplier_price + supplier_price * ( float(percentage_increase)/float(100) )

        sell_price = math.modf(sell_price) # (0.5678000000000338, 1234.0)

        # set minimumprice as minimum is the min_price is <
        if float(sell_price[1]) < float(minimumprice):
            minimumprice = math.modf(minimumprice)
            #round price
            sell_price = float(minimumprice[1]) + float(roundat)
        else:
            sell_price = float(sell_price[1]) + float(roundat)

        item_object.sellPrice = str(sell_price)

        return item_object

def set_variant_price(variant, percentage_increase, minimumprice, roundat, use_preset_price):
    supplier_price = float(variant.supplierSellPrice)

    if use_preset_price == 'on' or use_preset_price == True:
        sell_price = supplier_price
    else:
        sell_price = supplier_price + supplier_price * ( float(percentage_increase)/float(100) )
    
    sell_price = math.modf(sell_price) # (0.5678000000000338, 1234.0)
    # set minimumprice as minimum is the min_price is <
    if float(sell_price[1]) < float(minimumprice):
        minimumprice = math.modf(minimumprice)
        #round price
        sell_price = float(minimumprice[1]) + float(roundat)
    else:
        sell_price = float(sell_price[1]) + float(roundat)

    variant.sellPrice = float(sell_price)

    return variant

def parse_cj_categories(product_details):
    categories_string = product_details['categoryName']
    categories = re.split('> | /', categories_string)
    print(categories)
    categories_dict = { 'first': '',
                'second': '',
                 'third': '' }
    for i in range(len(categories)):
        if i == 0:
            categories_dict['first'] = categories[0]
        elif i == 1:
            categories_dict['second'] = categories[1]
        elif i == 2:
            categories_dict['third'] = categories[2]
    return categories_dict


def updateUserWords(user, tokens_used):
    words_used = int(round((int(tokens_used)/0.80), 0))
    #user_instance = CustomUser.objects.get(email=user.email)
    words = user.words
    user.words = words - words_used
    user.save()
