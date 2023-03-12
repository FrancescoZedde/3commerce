



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
            print(variant.variantSku)
            print(variant_values)
            variant_dict = {}
            for value in variant_values:
                print(value)
                for option in options_set:
                    if value in option["values"]:
                        option_position = "option" + str(option["position"])
                        variant_dict[option_position] = value

            variant_dict["sku"] = variant.variantSku
            variant_dict["price"] = variant.supplierSellPrice
            #variant_dict["attributes"] = {}
            #variant_dict["inventory_quantity"] = "50",
            #variant_dict["inventory_management"] =  "shopify",
            #variant_dict["inventory_quantity"] =  "99"
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
