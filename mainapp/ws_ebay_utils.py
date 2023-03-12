from mainapp.db_functions import retrieveItemBySku, retrieveVariantsByItem, retrieveVariantBySku
from mainapp.ws_cj import cj_get_inventory_inquiry
import base64
import re

'''
inventory items in Ebay = variants nell'app
items group Ebay = gruppo di varianti

'''


def base64_encode_credentials(client_id, client_secret):
   string_to_encode = client_id + ':' + client_secret
   string_bytes = string_to_encode.encode('ascii')
   base64_bytes = base64.b64encode(string_bytes)
   base64_credentials = base64_bytes.decode('ascii')
   basic_auth = 'Basic ' + base64_credentials
   return basic_auth

def ebay_create_json_inventory_item(item_sku):
   item = retrieveItemBySku(item_sku)
   variants = retrieveVariantsByItem(item)

   print('VARIANTI N°' + str(len(variants)))

   variants = ebay_remove_variants(variants)

   variants_item_list = []

   for variant in variants:
      inventory_inquiry = cj_get_inventory_inquiry(variant.vid)
      aspects = ebay_set_aspects(item, variant)
      #IN_STOCK,OUT_OF_STOCK,SHIP_TO_STORE
      json_inventory_item = {
                              "sku": variant.variantSku,
                              "availability":{
                              "pickupAtLocationAvailability":[],
                              "shipToLocationAvailability":{
                                     "availabilityDistributions":[
                                        {
                                           "merchantLocationKey":inventory_inquiry[0]["areaId"],
                                           "quantity":1,
                                        }
                                     ],
                                     "quantity":1,
                                  }
                               },
                               "condition":"NEW",
                               "conditionDescription":"Brand new",
                               "locale":"en_US",
                               "packageWeightAndSize":{
                                  "dimensions":{
                                     "height": variant.variantHeight,
                                     "length": variant.variantLength,
                                     "unit": "CENTIMETER",
                                     "width": variant.variantWidth
                                  },
                               },
                               "product":{
                                  "aspects": aspects,
                                  "description": variant.description,
                                  "imageUrls":[
                                     variant.variantImage
                                  ],
                                  "title": item.itemName,
                               }
                              }
      variants_item_list.append(json_inventory_item)

   payload = {"requests" : variants_item_list}

   print(payload)

   return payload


def ebay_create_json_inventory_item_group(item_sku):
   item = retrieveItemBySku(item_sku)
   variants = retrieveVariantsByItem(item)

   print('VARIANTI N°' + str(len(variants)))

   variants = ebay_remove_variants(variants)

   variant_skus_list = []
   specifications = ebay_set_specifications_items_group(item, variants)

   aspects = {}
   for spec in specifications['specifications']:
      aspects[spec['name']] = spec['values']


   image_urls_list = ebay_set_image_urls(item)


   for variant in variants:
      variant_skus_list.append(variant.variantSku)

   inventory_item_group_key = item.sku

   try:
      description = remove_footer_contact_information(item.descriptionTemplate)
   except:
      description = item.description
   #"aspects":{"patter": ["solid"]},
   payload =  {
                     "title": item.itemName,
                     "description": description,
                     "imageUrls": image_urls_list,
                     "variantSKUs": variant_skus_list,
                     "variesBy":{
                        "aspectsImageVariesBy":[
                           specifications['specifications'][0]["name"]
                        ],
                        "specifications":specifications['specifications']
                     }
                  }

   
   return inventory_item_group_key, payload



def ebay_create_json_offer(item_sku, price_multiplier):
   #retrieve categoryId
   
   item = retrieveItemBySku(item_sku)
   variants = retrieveVariantsByItem(item)

   variants = ebay_remove_variants(variants)

   print('VARIANTI N°' + str(len(variants)))
   offers_payload = []
   for variant in variants:
      #retrieve variant
      #variant = retrieveVariantBySku(sku)

      offer = {
                  "categoryId": "30120",
                  "format":"FIXED_PRICE",
                  "hideBuyerDetails":True,
                  #"listingDescription":"string",
                  "listingDuration":"GTC",
                  "listingPolicies": {
                     "fulfillmentPolicyId": "210762294025",
                     "returnPolicyId": "210762134025",
                     "paymentPolicyId": "210762267025",    
                  },
                  "marketplaceId": "EBAY_US",
                  "merchantLocationKey":"test-location-cn-warehouse-1612",
                  "pricingSummary":{
                     "price":{
                        "currency":"USD",
                        "value": str(variant.supplierSellPrice * int(price_multiplier) )
                     },
                  },
                  "sku": variant.variantSku,
               }
      offers_payload.append(offer)
   
   payload = {"requests": offers_payload}
   print('OFFERS PAYLOAD')
   print(payload)
   return payload


def ebay_remove_variants(variants):
   if len(variants) > 25:
      print('remove variants...')
      variants = variants[0:25]
      print(len(variants))
      return variants
   else:
      return variants


def ebay_set_aspects(item, variant):

   # attributes names from item
   attributes_names = item.attributes
   attributes_names = attributes_names.split("-")
   # attributes values from variant
   attributes_values = variant.variantKey
   attributes_values = attributes_values.split("-")

   aspects = {}

   for i in range(len(attributes_names)):
      arr = []
      arr.append(attributes_values[i])
      aspects[attributes_names[i]] = arr
   
   print(aspects)
   return aspects

def ebay_set_image_urls(item):
   image_urls_string = item.productImageSet.replace("'", '')
   image_urls_string = image_urls_string.replace("[", '')
   image_urls_string = image_urls_string.replace("]", '')
   image_urls_string = image_urls_string.replace(" ", '')

   image_urls_list = re.split(',', image_urls_string)

   return image_urls_list


def ebay_set_specifications_items_group(item, variants):

   attributes_names = item.attributes
   attributes_names = attributes_names.split("-")

   specifications = {"specifications" : []}

   for i in range(len(attributes_names)):
      single_spec = {
                     "name":attributes_names[i],
                     "values": []
                     }
      specifications["specifications"].append(single_spec)

   for variant in variants:
      attributes_values = variant.variantKey
      attributes_values = attributes_values.split("-")

      for i in range(len(attributes_values)):
         spec = specifications["specifications"][i]

         spec["values"].append(attributes_values[i])

   return specifications

def remove_footer_contact_information(description_template):
   new_description_template = description_template.replace('For any questions or assistance you can contact us by email at: <strong>hello@xzshop.eu</strong><br><br>or via WhatsApp:<strong>+39 351 281 1816</strong>', 'Do you need a larger quantity? Write us!')
   return new_description_template
#def ebay_create_json_offers():


'''
{
   "requests":[
      {
         "availableQuantity":"integer",
         "categoryId":"string",
         "charity":{
            "charityId":"string",
            "donationPercentage":"string"
         },
         "extendedProducerResponsibility":{
            "producerProductId":"string",
            "productPackageId":"string",
            "shipmentPackageId":"string",
            "productDocumentationId":"string",
            "ecoParticipationFee":{
               "currency":"string",
               "value":"string"
            }
         },
         "format":"FormatTypeEnum : [AUCTION,FIXED_PRICE]",
         "hideBuyerDetails":"boolean",
         "includeCatalogProductDetails":"boolean",
         "listingDescription":"string",
         "listingDuration":"ListingDurationEnum : [DAYS_1,DAYS_3,DAYS_5...]",
         "listingPolicies":{
            "bestOfferTerms":{
               "autoAcceptPrice":{
                  "currency":"string",
                  "value":"string"
               },
               "autoDeclinePrice":{
                  "currency":"string",
                  "value":"string"
               },
               "bestOfferEnabled":"boolean"
            },
            "eBayPlusIfEligible":"boolean",
            "fulfillmentPolicyId":"string",
            "paymentPolicyId":"string",
            "productCompliancePolicyIds":[
               "string"
            ],
            "returnPolicyId":"string",
            "shippingCostOverrides":[
               {
                  "additionalShippingCost":{
                     "currency":"string",
                     "value":"string"
                  },
                  "priority":"integer",
                  "shippingCost":{
                     "currency":"string",
                     "value":"string"
                  },
                  "shippingServiceType":"ShippingServiceTypeEnum : [DOMESTIC,INTERNATIONAL]",
                  "surcharge":{
                     "currency":"string",
                     "value":"string"
                  }
               }
            ],
            "takeBackPolicyId":"string"
         },
         "listingStartDate":"string",
         "lotSize":"integer",
         "marketplaceId":"MarketplaceEnum : [EBAY_US,EBAY_MOTORS,EBAY_CA...]",
         "merchantLocationKey":"string",
         "pricingSummary":{
            "auctionReservePrice":{
               "currency":"string",
               "value":"string"
            },
            "auctionStartPrice":{
               "currency":"string",
               "value":"string"
            },
            "minimumAdvertisedPrice":{
               "currency":"string",
               "value":"string"
            },
            "originallySoldForRetailPriceOn":"SoldOnEnum : [ON_EBAY,OFF_EBAY,ON_AND_OFF_EBAY]",
            "originalRetailPrice":{
               "currency":"string",
               "value":"string"
            },
            "price":{
               "currency":"string",
               "value":"string"
            },
            "pricingVisibility":"MinimumAdvertisedPriceHandlingEnum : [NONE,PRE_CHECKOUT,DURING_CHECKOUT]"
         },
         "quantityLimitPerBuyer":"integer",
         "secondaryCategoryId":"string",
         "sku":"string",
         "storeCategoryNames":[
            "string"
         ],
         "tax":{
            "applyTax":"boolean",
            "thirdPartyTaxCategory":"string",
            "vatPercentage":"number"
         }
      }
   ]
}

def ebay_create_json_bulk_create_or_replace_inventory_item(sku_list):
    inventory_items_list = []
    for sku in sku_list:
        json_inventory_item = create_json_inventory_item(sku)
        inventory_items_list.append(json_inventory_item)

    payload = {"requests" : inventory_items_list}

    return payload

{
   "requests":[
      {
         "availability":{
            "pickupAtLocationAvailability":[
               {
                  "availabilityType":"AvailabilityTypeEnum : [IN_STOCK,OUT_OF_STOCK,SHIP_TO_STORE]",
                  "fulfillmentTime":{
                     "unit":"TimeDurationUnitEnum : [YEAR,MONTH,DAY...]",
                     "value":"integer"
                  },
                  "merchantLocationKey":"string",
                  "quantity":"integer"
               }
            ],
            "shipToLocationAvailability":{
               "availabilityDistributions":[
                  {
                     "fulfillmentTime":{
                        "unit":"TimeDurationUnitEnum : [YEAR,MONTH,DAY...]",
                        "value":"integer"
                     },
                     "merchantLocationKey":"string",
                     "quantity":"integer"
                  }
               ],
               "quantity":"integer"
            }
         },
         "condition":"ConditionEnum : [NEW,LIKE_NEW,NEW_OTHER...]",
         "conditionDescription":"string",
         "locale":"LocaleEnum : [en_US,en_CA,fr_CA...]",
         "packageWeightAndSize":{
            "dimensions":{
               "height":"number",
               "length":"number",
               "unit":"LengthUnitOfMeasureEnum : [INCH,FEET,CENTIMETER...]",
               "width":"number"
            },
            "packageType":"PackageTypeEnum : [LETTER,BULKY_GOODS,CARAVAN...]",
            "weight":{
               "unit":"WeightUnitOfMeasureEnum : [POUND,KILOGRAM,OUNCE...]",
               "value":"number"
            }
         },
         "product":{
            "aspects":"string",
            "brand":"string",
            "description":"string",
            "ean":[
               "string"
            ],
            "epid":"string",
            "imageUrls":[
               "string"
            ],
            "isbn":[
               "string"
            ],
            "mpn":"string",
            "subtitle":"string",
            "title":"string",
            "upc":[
               "string"
            ],
            "videoIds":[
               "string"
            ]
         },
         "sku":"string"
      }
   ]
}

payload = {
    "requests": [
        {
            "sku": "XZTESTSKU000",
            "locale": "en_US",
            "product": {
                "title": "Boston Terriers Collector Plate &quot;All Ears by Dan Hatala - The Danbury Mint",
                "aspects": {
                    "Country/Region of Manufacture": [
                        "United States"
                    ]
                },
                "description": "All Ears by Dan Hatala. A limited edition from the collection entitled 'Boston Terriers'. Presented by The Danbury Mint.",
            },
            "condition": "USED_EXCELLENT",
            "conditionDescription": "Mint condition. Kept in styrofoam case. Never displayed.",
            "availability": {
                "shipToLocationAvailability": {
                    "quantity": 2
                }
            }
        },
        {
            "sku": "XZTESTSKU001",
            "locale": "en_US",
            "product": {
                "title": "JOE PAVELSKI 2015-16 BOBBLEHEAD NHL SAN JOSE SHARKS 25TH ANNIVERSARY",
                "aspects": {
                    "Team": [
                        "San Jose Sharks"
                    ],
                    "Player": [
                        "Joe Pavelski"
                    ],
                    "Pre & Post Season": [
                        "Regular Season"
                    ],
                    "Product": [
                        "Bobblehead"
                    ],
                    "Country/Region of Manufacture": [
                        "China"
                    ],
                    "Brand": [
                        "Success Promotions"
                    ],
                    "UPC": [
                        "Does not apply"
                    ]
                },
                "description": "Joe Pavelski bobble head from 2015-16 season, the 25th season of the San Jose Sharks. New in box.",
            },
            "condition": "NEW",
            "availability": {
                "shipToLocationAvailability": {
                    "quantity": 1
                }
            }
        }
    ]
}
'''