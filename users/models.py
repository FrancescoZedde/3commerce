from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):

    status = (
        ('regular', 'regular'),
        ('subscriber', 'subscriber'),
        ('moderator', 'moderator')
    )

    store_tipologies= (
        ('none', 'None'),
        ('woocommerce', 'WooCommerce'),
        ('shopify', 'Shopify')
        )

   
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=status, default='regular')

    # WORD CREDITS
    words = models.IntegerField( default=2000)

    # EBAY
    ebay_access_token = models.TextField('Ebay Access Token', default='', blank=True)

    # FACEBOOK/INSTAGRAM
    facebook_user_id = models.TextField('Facebook User ID', default='', blank=True)
    facebook_page_id = models.TextField('Facebook Page ID', default='', blank=True)
    instagram_user_id = models.TextField('Instagram User ID', default='', blank=True)
    facebook_access_token = models.TextField('Facebook Access Token', default='', blank=True)

    # STORE TYEP
    store_type = models.CharField(max_length=20, choices=store_tipologies, default="none")
    store_name = models.TextField('Store name', default='', blank=True)

    # WOOCOMMERCE
    woocommerce_store_name = models.TextField('WooCommerce store name', default='', blank=True)
    woocommerce_host = models.TextField('WooCommerce store domain', default='', blank=True)
    woocommerce_consumer_key = models.TextField('WooCommerce consumer key', default='', blank=True)
    woocommerce_secret_key = models.TextField('WooCommerce secret key', default='', blank=True)

    #SHOPIFY
    shopify_store_name = models.TextField('Shopify store name', default='', blank=True)
    shopify_host = models.TextField('Shopify store domain', default='', blank=True)
    shopify_consumer_key = models.TextField('Shopify consumer key', default='', blank=True)
    shopify_secret_key = models.TextField('Shopify secret key', default='', blank=True)

    # CJ DROPSHIPPING
    cjdropshipping_email = models.TextField('CJDropshipping Email', default='', blank=True)
    cjdropshipping_api_key = models.TextField('CJDropshipping API Key', default='', blank=True)
      
    description = models.TextField('Description', max_length=600, default='', blank=True)

    def _str_(self):
        return self.username


class Order(models.Model):

    order_status_choices = (
        ('pending', 'Pending'),
        ('submited', 'Submited'),
        ('fulfilled', 'FulFilled')
    )

    user = models.ForeignKey(CustomUser, related_name='user',on_delete=models.CASCADE,)
    external_order_id = models.TextField('External order id:', max_length=10000, default='', blank=True)
    #store_name = models.CharField('Store Name', max_length=255, default='', blank=True)
    status = models.CharField(max_length=20, choices=order_status_choices, default="Pending")
    order_info =  models.TextField('Full JSON response:', max_length=10000, default='', blank=True)
    shipping_zip = models.CharField('Shipping Zip', max_length=10, default='', blank=True)
    shipping_country_code = models.CharField('Shipping Country Code', max_length=10, default='', blank=True)
    shipping_country = models.CharField('Shipping Country', max_length=100, default='', blank=True)
    shipping_province = models.CharField('Shipping Province', max_length=100, default='', blank=True)
    shipping_city = models.CharField('Shipping City', max_length=100, default='', blank=True)
    shipping_address = models.TextField('Shipping Address', max_length=500, default='', blank=True)
    shipping_customer_name = models.CharField('Shipping Customer Name', max_length=100, default='', blank=True)
    shipping_phone = models.CharField('Shipping Phone', max_length=20, default='', blank=True)
    remark = models.TextField('Remark', max_length=500, default='', blank=True)
    from_country_code = models.CharField('From Country Code', max_length=10, default='', blank=True)
    logistic_name = models.CharField('Logistic Name', max_length=100, default='', blank=True)
    products = models.TextField('Products', max_length=1000, default='', blank=True)
    vids = models.TextField('Products', max_length=1000, default='', blank=True)