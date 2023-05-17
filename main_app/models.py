from django.db import models
from users_app.models import CustomUser
# Create your models here.
'''sku
supplier
supplierSku
categoryFirst
categorySecond
categoryThird
categoryFourth


jsonDataImported
jsonWooCommerceImport
jsonEbayImport'''

'''
class Shop(model.Model):
    host = models.TextField()
    public =
    secret = '''

class InventoryItem(models.Model):
    user = models.ForeignKey(CustomUser, related_name='variant',on_delete=models.CASCADE,)
    sku = models.TextField()
    itemName = models.TextField()
    description = models.TextField()
    descriptionTemplate = models.TextField()
    descriptionFeatures = models.TextField()
    descriptionCustom = models.TextField()
    supplierSellPrice = models.TextField()
    sellPrice = models.TextField()
    supplier = models.TextField()
    supplierSku = models.TextField()
    brand = models.TextField(blank=True)
    woocommerceId = models.TextField()
    categoryFirst = models.TextField()
    categorySecond = models.TextField()
    categoryThird = models.TextField()
    categoryFourth = models.TextField()
    attributes = models.TextField()
    productWeight = models.TextField()
    productType = models.TextField()
    entryNameEn = models.TextField()
    materialNameEn = models.TextField()
    packingWeight = models.TextField()
    productImage= models.TextField()
    productImageSet= models.TextField()
    jsonDataImported = models.TextField()
    jsonVariants = models.TextField()
    jsonWooCommerceExport = models.TextField()
    jsonWooCommerceExportVariants = models.TextField()
    jsonEbayExportCreateInventoryItems = models.TextField()
    jsonEbayExportCreateItemsGroup = models.TextField()
    jsonEbayExportCreateOffers = models.TextField()
    onsaleWoocommerce = models.BooleanField(default=False)
    onsaleEbay = models.BooleanField(default=False)
    outOfStock = models.BooleanField(default=False)
    ebayCategory = models.TextField()
    #jsonEbayExportInventoryItems = models.TextField()


class Variant(models.Model):
    item = models.ForeignKey(InventoryItem, related_name='variant',on_delete=models.CASCADE,)
    variantSku = models.TextField()
    vid = models.TextField()
    variantNameEn = models.TextField(null=True)
    description = models.TextField()
    supplierSellPrice = models.FloatField()
    sellPrice = models.FloatField()
    supplier = models.TextField()
    supplierSku = models.TextField()
    variantImage= models.TextField()
    variantKey= models.TextField()
    variantLength= models.TextField()
    variantWidth= models.TextField()
    variantHeight= models.TextField()
    variantVolume= models.TextField()
    variantWeight= models.TextField()
    areaId = models.TextField()
    storageNum =models.TextField()
    countryCode = models.TextField()
    allLocations = models.TextField()
    firstShippingMethod = models.TextField()
    secondShippingMethod = models.TextField()
    thirdShippingMethod = models.TextField()
    allShippingMethods  =models.TextField()
    onsaleWoocommerce = models.BooleanField(default=False)
    onsaleEbay = models.BooleanField(default=False)
    outOfStock = models.BooleanField(default=False)
    
    #shipping informations

class WoocommerceStore(models.Model):
    name = models.CharField(max_length=155)
    url = models.CharField(max_length=155)
    ck = models.CharField(max_length=155)
    cs = models.CharField(max_length=155)