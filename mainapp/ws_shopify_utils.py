
import re


class ShopifyUtils:

    def shopify_set_options(attributes, variants):
        
        print(attributes)
        attributes = attributes.split("-")
        options = []
        for i in range(len(attributes)):        
            option = {
                    "position": i + 1,
                    "name": attributes[i].capitalize(),
                    "values": []
                    }
            options.append(option)
        
        for variant in variants:
            variant_values = variant.variantKey
            variant_values = variant_values.split("-")

            for i in range(len(variant_values)):
                if variant_values[i] not in options[i]["values"]:
                    options[i]["values"].append(variant_values[i])
        
        print(options)
        return options

    def shopify_set_variants(options_set, variants):
        variants_set = []
        for variant in variants:
            variant_values = variant.variantKey
            variant_values = variant_values.split("-")

            variant_dict = {}
            for value in variant_values:
                print(value)
                for option in options_set:
                    if value in option["values"]:
                        option_position = "option" + str(option["position"])
                        variant_dict[option_position] = value

            variant_dict["sku"] = variant.variantSku
            variant_dict["price"] = variant.supplierSellPrice

            variants_set.append(variant_dict)
        print(variants_set)
        print(variants_set[0])
        return variants_set


    def shopify_set_images(productImageSet):
        img_set = []
        for image in productImageSet:
            img = {'src': image}
            img_set.append(img)
        return img_set

    
    def shopify_match_skus_images_ids(variants, create_product_response):
        shopify_images = create_product_response["product"]["images"]
        shopify_variants = create_product_response["product"]["variants"]

        shopify_variants_dict = {}
        for shopify_variant in shopify_variants:
            shopify_variants_dict[shopify_variant['sku']] = shopify_variant['id']
        images_names_shopify = {}
        for image in shopify_images:
            name = ShopifyUtils.find_between_strings(image["src"], "https://cdn.shopify.com/s/files/1/0733/8105/2714/products/", "?v=")
            images_names_shopify[name] = image['id']

        images_names_sellfast = {}
        for variant in variants:
            name = variant.variantImage[variant.variantImage.rindex('/')+1:]
            images_names_sellfast[variant.variantSku] = name
        
        return shopify_variants_dict, images_names_shopify, images_names_sellfast


    def find_between_strings( s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""
