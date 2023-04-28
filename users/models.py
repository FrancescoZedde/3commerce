from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):

    status = (
        ('free', 'free'),
        ('basic', 'basic'),
        ('premium', 'premium'),
        ('moderator', 'moderator')
    )

    store_tipologies= (
        ('none', 'None'),
        ('woocommerce', 'WooCommerce'),
        ('shopify', 'Shopify')
        )

   
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=status, default='free')

    # WORD CREDITS
    words = models.IntegerField(default=2000)

    # SEARCHES
    searches = models.IntegerField(default=0)

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

    user = models.ForeignKey(CustomUser, related_name='user_order',on_delete=models.CASCADE,)
    external_order_id = models.TextField('External order id:', max_length=10000, default='', blank=True)
    store_name = models.CharField('Store Name', max_length=255, default='', blank=True)
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


class ContractOrder(models.Model):

    status_options = (
        ('pending', 'pending'),
        ('failed', 'failed'),
        ('succed', 'succed')
    )

    user = models.ForeignKey(CustomUser, related_name='user_contract_order', on_delete=models.PROTECT)
    timestamp = models.TextField('timestamp', default='', blank=True)
    status = models.TextField(max_length=20, choices=status_options, default="pending")
    lookup_key = models.TextField('lookup key', default='')
    session_id = models.TextField('session if', default='', blank=True)



class CheckoutSession(models.Model):
    api_version = models.TextField(default='', blank=True)
    created = models.TextField(default='', blank=True)
    amount_subtotal = models.TextField(default='', blank=True)
    amount_total = models.TextField(default='', blank=True)
    billing_address_collection = models.TextField(default='', blank=True)
    cancel_url = models.TextField(default='', blank=True)
    created = models.TextField(default='', blank=True)
    currency = models.TextField(default='', blank=True)
    customer = models.TextField(default='', blank=True)
    customer_creation = models.TextField(default='', blank=True)
    customer_email = models.TextField(default='', blank=True)
    expires_at = models.TextField(default='', blank=True)
    session_id = models.TextField(primary_key=True, default='', blank=True)
    invoice = models.TextField(default='', blank=True)
    livemode = models.TextField(default='', blank=True)
    mode = models.TextField(default='', blank=True)
    object_type = models.TextField(default='', blank=True)
    payment_method_collection = models.TextField(default='', blank=True)
    payment_method_types = models.TextField(default='', blank=True)
    payment_status = models.TextField(default='', blank=True)
    phone_number_collection = models.TextField(default='', blank=True)
    status = models.TextField(default='', blank=True)
    subscription = models.TextField(default='', blank=True)
    success_url = models.TextField(default='', blank=True)
    total_details = models.TextField(default='', blank=True)
    session_type = models.TextField(default='', blank=True)