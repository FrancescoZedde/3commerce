from mainapp.db_functions import retrieveItemBySku, create_item_and_variants
from mainapp.ws_cj import cj_products_by_category, cj_get_product_details
from mainapp.forms import InventoryItemForm, VariantForm
import math
from ast import literal_eval
import re


def remove_img_tags(description_string):
    p = re.compile(r'<img.*?>')
    return p.sub('', description_string)

#def build_body_default_template(item):


def create_default_template_description_string(item):
    #item = retrieveItemBySku(item_sku)
    header_1 = '<table style="width: 100%; border: none;" cellspacing="0" cellpadding="0"><tbody><tr><th style="width: 100%; text-align: center;"></th></tr><tr><td style="text-align: center;"><h2>'
    header_2 = '</h2></td></tr></tbody></table>'

    footer = '<table id="template-footer" style="width:100%;border:none" cellspacing="0" cellpadding="0"><tbody><tr><th style="width:33%;text-align:center"><h4>Shipping</h4></th><th style="width:33%;text-align:center"><h4>Support</h4></th></tr><tr><td style="text-align:center">We strive to deliver as soon as possible. Once your order is confirmed you will receive a tracking code to stay updated on the status of the shipment<br><img class="aligncenter" style="width:61px;height:61px" src="https://xzshop.eu/wp-content/uploads/2023/02/shipped.png"></td><td style="text-align:center">We provide 24/7 support and assistance for every order. Contact us anytime by email or whatsapp. We usually respond in 12-24 hours.<br><img class="aligncenter" style="width:61px;height:61px" src="https://xzshop.eu/wp-content/uploads/2023/02/support.png"></td></tr></tbody></table><table style="width:100%;border:none" cellspacing="0" cellpadding="0"><tbody><tr><th style="width:20%;text-align:center"></th><th style="width:80%;text-align:center"></th></tr><tr><td style="text-align:center"><img class="alignnone wp-image-4707" src="https://electronics.xzshop.eu/wp-content/uploads/2023/01/cropped-cropped-xz-300x300.png" alt="" width="126" height="126"></td><td style="text-align:left;margin-left:1em">For any questions or assistance you can contact us by email at: <strong>hello@xzshop.eu</strong><br><br>or via WhatsApp:<strong>+39 351 281 1816</strong></td></tr></tbody></table>'

    img_set = literal_eval(item.productImageSet)

    if item.descriptionChatGpt == '':
        body_1 = '<table style="width: 100%; border: none;" cellspacing="0" cellpadding="0"><tbody><tr><th style="width: 50%;"></th><th style="width: 50%;"></th></tr><tr><td>'
        body_2 = '</td></tr></tbody></table>'
        footer_img_set_1 = '<table style="width: 100%; border: none;" cellspacing="0" cellpadding="0"><tbody><tr><th></th><th></th><th></th></tr><tr>'
        footer_img_set_2 = '</tr></tbody></table>'

        body_img_set_string = ''
        footer_img_set_string = ''

        if len(img_set) >= 2:
            for i in range(2):
                img_tag_1 = '<img style="width: 100%;" src="'
                img_tag_2 = '" />'
                img_tag = img_tag_1 + str(img_set[i]) + img_tag_2 
                body_img_set_string = body_img_set_string + img_tag + '<br>'
                del img_set[i]

        for img in img_set:
            img_tag_1 = '<td><img style="width: 100%;" src="'
            img_tag_2 = '" /></td>'
            img_tag = img_tag_1 + str(img) + img_tag_2
            footer_img_set_string = footer_img_set_string + img_tag

        description_without_img_tags = remove_img_tags(item.description)

        stringTemplateDescription = header_1 + str(item.itemName) + header_2 + body_1 + body_img_set_string + '</td><td>' + '<div id="text-description" style="margin-left:2em">' + description_without_img_tags + '</div>' + body_2 + footer_img_set_1 + footer_img_set_string + footer_img_set_2 + footer
    else:
        img_counts = len(img_set)
        n_img_rows_raw = img_counts/3
        n_img_rows_raw_rounded = math.ceil(n_img_rows_raw)
        print(n_img_rows_raw)
        print(n_img_rows_raw_rounded)
        img_table_start = '<table style="width:100%;border:none" cellspacing="0" cellpadding="0"><tbody><tr><th></th><th></th><th></th></tr>'
        img_table_body = ''
        img_table_end = '</tbody></table>'
        for i in range(n_img_rows_raw_rounded):
            img_table_row = ''
            for t in range(1,4):
                print(t)
                img_tag_1 = '<td><img style="width: 100%;" src="'
                img_tag_2 = '" /></td>'
                try:
                    img_tag = img_tag_1 + str(img_set[t-1]) + img_tag_2
                    img_table_row = img_table_row + img_tag
                except:
                    pass
                
            try:
                del img_set[:3]
            except:
                break
            img_table_row = '<tr>' + img_table_row + '</tr>'

            img_table_body = img_table_body + img_table_row
        
        img_table_full = img_table_start + img_table_body + img_table_end
        #print('IMG TABLE FULL')
        #print(img_table_full)
        if item.descriptionFeatures == '':
            stringTemplateDescription = header_1 + str(item.itemName) + header_2 + '<div id="text-description">' + item.descriptionChatGpt + '</div>' + img_table_full + footer
        else:
            features = set_format_features_description(item.descriptionFeatures)
            stringTemplateDescription = header_1 + str(item.itemName) + header_2 + '<div id="text-description">' + item.descriptionChatGpt + '</div>' + '<div style="max-width:80%; margin-top:1em;">' + features + '</div>' + img_table_full + footer
        print('FULL DESC')
        print(stringTemplateDescription)


    print(stringTemplateDescription)
    item.descriptionTemplate = stringTemplateDescription

    item.save()


def set_format_features_description(description_features):
    print(description_features)
    features_1 = '<ul>'
    features_2 = '</ul>'
    features_body = ''
    for line in description_features.splitlines():
        print(line)
        features_body = features_body + '<li>' + line + '</li>'
    features = features_1 + features_body + features_2
    return features

def create_template_description_string(request, template_n):
    #retrieve product by sku
    print(request)

    item = retrieveItemBySku(request['selected-item'])
    print(item)
    if template_n == '0':
        print('template 0')

        '''
        custom_html = request['customHTML']

        stringTemplateDescription = header_1 + title + header_2 + footer

        item.descriptionTemplate = stringTemplateDescription

        item.save()'''

    elif template_n == '1':

        title = request['title']
        image1 = '<td><img style="width: 100%;" src="' + request['urlimage1'] + '" /></td>'
        image2 = '<td><img style="width: 100%;" src="' + request['urlimage2'] + '" /></td>'
        image3 = '<td><img style="width: 100%;" src="' + request['urlimage3'] + '" /></td>'
        image4 = '<td><img style="width: 100%;" src="' + request['urlimage4'] + '" /></td>'
        image5 = '<td><img style="width: 100%;" src="' + request['urlimage5'] + '" /></td>'

        text1 = request['text1']
        text2 = request['text2']
        
        header_1 = '<table style="width:100%;border:none" cellspacing="0" cellpadding="0"><tbody><tr><th style="width:20%;text-align:center"></th><th style="width:80%;text-align:center"></th></tr><tr><td style="text-align:center"><img class="alignnone wp-image-4707" src="https://electronics.xzshop.eu/wp-content/uploads/2023/01/cropped-cropped-xz-300x300.png" alt="" width="126" height="126"></td><td style="text-align:center"><h2>'
        header_2 = '</h2></td></tr></tbody></table>'

        row1_1 = '<table style="width:100%;border:none" cellspacing="0" cellpadding="0"><tbody><tr><th style="width:50%"></th><th style="width:50%"></th></tr><tr>'
        
        row1_2 = '</td></tr></tbody></table>'

        imgset_1 = '&nbsp;<table style="width:100%;border:none" cellspacing="0" cellpadding="0"><tbody><tr><th></th><th></th><th></th></tr><tr>'
        imgset_2 = '</tr></tbody></table>'

        footer = '<table style="width:100%;border:none" cellspacing="0" cellpadding="0"><tbody><tr><th style="width:33%;text-align:center">Shipping</th><th style="width:33%;text-align:center">24/7</th><th style="width:33%;text-align:center">Return policy</th></tr><tr><td style="text-align:center">We strive to deliver as soon as possible, once your order is confirmed you will receive a tracking code.</td><td style="text-align:center">We provide 24/7 free assisitance, you can contact us by email or WhatsApp. We usually respond in 12-24 hours.</td><td style="text-align:center">Our return policy allows you to return the product up to 30 days after you receive it.</td></tr></tbody></table><table style="width:100%;border:none" cellspacing="0" cellpadding="0"><tbody><tr><th style="width:20%;text-align:center"></th><th style="width:80%;text-align:center"></th></tr><tr><td style="text-align:center"><img class="alignnone wp-image-4707" src="https://electronics.xzshop.eu/wp-content/uploads/2023/01/cropped-cropped-xz-300x300.png" alt="" width="126" height="126"></td><td style="text-align:left;margin-left:1em">For any questions or assistance you can contact us by email at:<strong>hello@xzshop.eu</strong>or via WhatsApp:<strong>+39</strong></td></tr></tbody></table>'

        stringTemplateDescription = header_1 + title + header_2 + row1_1 + image1 + '<td>' + text1 + '</td></tr><tr>' + image2 + '<td>' +text2 + row1_2 + imgset_1 + image3 + image4 + image5 + imgset_2 + footer

        item.descriptionTemplate = stringTemplateDescription

        item.save()

    elif template_n == '2':
        header_1 = '<table style="width:100%;border:none" cellspacing="0" cellpadding="0"><tbody><tr><th style="width:20%;text-align:center"></th><th style="width:80%;text-align:center"></th></tr><tr><td style="text-align:center"><img class="alignnone wp-image-4707" src="http://xzshop.eu/wp-content/uploads/2023/01/cropped-xz-1.png" alt="" width="126" height="126"></td><td style="text-align:center"><h2>'
        title = request['title']
        print('TITLE------->' + str(title))
        header_2 = '</h2></td></tr></tbody></table>'
        footer = '<table style="width:100%;border:none" cellspacing="0" cellpadding="0"><tbody><tr><th style="width:33%;text-align:center">Shipping</th><th style="width:33%;text-align:center">24/7</th><th style="width:33%;text-align:center">Return policy</th></tr><tr><td style="text-align:center">We strive to deliver as soon as possible, once your order is confirmed you will receive a tracking code.</td><td style="text-align:center">We provide 24/7 free assisitance, you can contact us by email or WhatsApp. We usually respond in 12-24 hours.</td><td style="text-align:center">Our return policy allows you to return the product up to 30 days after you receive it.</td></tr></tbody></table><table style="width:100%;border:none" cellspacing="0" cellpadding="0"><tbody><tr><th style="width:20%;text-align:center"></th><th style="width:80%;text-align:center"></th></tr><tr><td style="text-align:center"><img class="alignnone wp-image-4707" src="https://electronics.xzshop.eu/wp-content/uploads/2023/01/cropped-cropped-xz-300x300.png" alt="" width="126" height="126"></td><td style="text-align:left;margin-left:1em">For any questions or assistance you can contact us by email at:<strong>hello@xzshop.eu</strong>or via WhatsApp:<strong>+39</strong></td></tr></tbody></table>'

        stringTemplateDescription = header_1 + title + header_2 + footer

        item.descriptionTemplate = stringTemplateDescription

        item.save()




def make_sku_list(items_list, sync_id):
    skus = []
    if sync_id == 'app-inventory':
        for item in items_list:
            skus.append(item.sku[2:])
    elif sync_id == 'sync-woocommerce':
        #print(len(items_list))
        for item in items_list:
            skus.append(item['sku'][2:])
    elif sync_id == 'sync-ebay':
        print(items_list)

    return skus

def compare_lists_and_import_missing_products(inventory_sku_list, shop_sku_list):
    results = []
    for sku in shop_sku_list:
        if sku in inventory_sku_list:
            print('do nothing')
        else:
            print('call cj to import item')
            try:
                product_details = cj_get_product_details(sku)
                inventory_item = create_item_and_variants(product_details)
                results.append({sku:'imported'})
            except:
                #print('prodotto non trovato')
                results.append({sku:'not found'})
    
    print(results)


def filter_by_keywords(products, keywords):
    new_list = []
    keywords = keywords.split()
    for product in products:
        for keyword in keywords:
            print(keyword)
            print(product['productNameEn'].lower().split())
            if keyword in product['productNameEn'].lower().split():
                new_list.append(product)
    return new_list


def create_item_and_variants_forms(item, variants):
    form_dict = {}
    item_form = InventoryItemForm(instance=item)
    form_dict['item_form'] = item_form
    variants_forms_list = []
    for variant in variants:
        variant_form = VariantForm(instance=variant)
        variants_forms_list.append(variant_form)
    form_dict['variants_forms'] = variants_forms_list
    return form_dict

def clean_html(raw_html):
    #raw_html = remove_img_tags(raw_html)
    cleaner = re.compile('<.*?>') 
    cleantext = re.sub(cleaner, '', raw_html)
    cleantext = cleantext[:600]
    return cleantext
#def update_inventory_after_sync()

def make_woocommerce_on_sale_products_list(woocommerce_products):
    products = []
    for product in woocommerce_products:
        p = {}
        p['id'] = product['id']
        p['sku'] = product['sku']
        p['name'] = product['name']
        p['url'] = product['permalink']
        p['mainImage'] = product['images'][0]['src']
        p['images'] = product['images']

        products.append(p)
    return products

def woocommerce_get_first_10_images(woocommerce_product):
    if len(woocommerce_product['images']) > 10:
        first_10_images = woocommerce_product['images'][0:10]
    else:
        first_10_images = woocommerce_product['images']
    image_set = []
    for image in first_10_images:
        image_set.append(image['src'])
    return image_set


def woocommerce_extract_text_description(description):
    result = re.search('<div id=\"text-description\"(.*)</div>', description)
    print(result)
    
    return result.group(1)


def format_results(list_of_products, elements_for_row):
    
    rows_plus_one = float(len(list_of_products)/elements_for_row)
    rows_plus_one = math.ceil(rows_plus_one)

    grouped_products_list = []
    for i in range(rows_plus_one):
        try:
            first_n_elements = list_of_products[0:elements_for_row] 
            grouped_products_list.append(first_n_elements)
        except:
            break
        try:
            del list_of_products[:elements_for_row]
        except:
            break

    return grouped_products_list