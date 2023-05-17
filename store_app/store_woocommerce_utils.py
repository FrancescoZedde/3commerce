



def create_jsonWooCommerceAddVariants(product_id, product_details):
    #wcapi = get_woocommerce_auth()
    #endpoint = "products/"+str(product_id)+"/variations/batch"
    
    attributes_names = product_details['productKeyEn']
    attributes_names = attributes_names.split("-")
    
    variants = product_details['variants']
    
    variants_list = []
    
    for variant in variants:
        variant_values = variant['variantKey']
        variant_values = variant_values.split("-")
        get_shipping_methods(variant['vid'])
        attributes = []
        for i in range(len(variant_values)):
            single_attribute = { "name": attributes_names[i], "option": variant_values[i]}
            attributes.append(single_attribute)
                
        variant_data = { "regular_price": str(set_price(variant['variantSellPrice'])),
                         "sku": variant['variantSku'],
                         "attributes":attributes
                       }
        variants_list.append(variant_data)
            
                
                
    jsonWooCommerceAddVariants = {"create": variants_list}
    
    print(jsonWooCommerceAddVariants)
            
    #response = wcapi.post(endpoint, data).json()
    
    #print(response)
    
    return jsonWooCommerceAddVariants



def woocommerce_set_attributes(product_details):
    attributes = product_details['productKeyEn']
    attributes = attributes.split("-")
    attributes_array_dict = []
    for i in range(len(attributes)):        
        single_attribute_dict = {
                'id':i,
                'attributeName': attributes[i],
                'options': []
                }
        attributes_array_dict.append(single_attribute_dict)
    variants = product_details['variants']
    for variant in variants:
        variant_values = variant['variantKey']
        variant_values = variant_values.split("-")
        for i in range(len(variant_values)):
            if variant_values[i] not in attributes_array_dict[i]['options']:
                attributes_array_dict[i]['options'].append(variant_values[i])
    attrbs = []
    for attribute in attributes_array_dict:
        a = {  #"id": attribute['id'],
                "name": attribute['attributeName'],
                "visible": "true",
                "variation": "true",
                "options": attribute['options']}
        attrbs.append(a)
        
    #set default attributes
    default_attributes = []
    for attrb in attrbs:
        try:
            default_attributes.append({'name':attrb['name'], 'option': attrb['options'][0]})
        except:
            pass
    return attrbs, default_attributes


    
def set_attributes(woocommerce_categories, product_details):
    
    categories_list = []
    for category in woocommerce_categories:
        cat = {'id': category['id'], 'name':category['slug']}
        categories_list.append(cat)
    print(categories_list)
    
    product_categories = []
    
    attributes = product_details['productKeyEn']
    attributes = attributes.split("-")
    attributes_array_dict = []
    for i in range(len(attributes)):        
        single_attribute_dict = {
                'id':i,
                'attributeName': attributes[i],
                'options': []
                }
        attributes_array_dict.append(single_attribute_dict)
            
    variants = product_details['variants']
    for variant in variants:
        variant_values = variant['variantKey']
        variant_values = variant_values.split("-")
        
        
        
        for i in range(len(variant_values)):
            if variant_values[i] not in attributes_array_dict[i]['options']:
                attributes_array_dict[i]['options'].append(variant_values[i])
        try:
            model_string = variant_values[1].lower()
            model_string = re.sub('[^A-Za-z0-9]+', '', model_string)
            print(model_string)
            category_match = False
            category_match = next(category for category in categories_list if category["name"] == model_string)#variant_values[1]
            if category_match != False:
                product_categories.append({'id':category_match['id']})
                print('here-category-match')
        except:
            pass
                
    # build final attributes structure
    attrbs = []
    print('attributes_array_dict')
    print(attributes_array_dict)
    for attribute in attributes_array_dict:
        a = {  #"id": attribute['id'],
                "name": attribute['attributeName'],
                "visible": "true",
                "variation": "true",
                "options": attribute['options']}
        attrbs.append(a)
        
    #set default attributes
    default_attributes = []
    for attrb in attrbs:
        try:
            default_attributes.append({'name':attrb['name'], 'option': attrb['options'][0]})
        except:
            pass
    #list comprhension remove categories duplicates
    product_categories = [i for n, i in enumerate(product_categories) if i not in product_categories[n + 1:]]
    if len(product_categories) == 0:
        product_categories.append({'id':83})
    
    return attrbs, default_attributes, product_categories