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