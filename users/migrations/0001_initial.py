# Generated by Django 3.2.3 on 2023-04-16 14:03

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('status', models.CharField(choices=[('regular', 'regular'), ('subscriber', 'subscriber'), ('moderator', 'moderator')], default='regular', max_length=100)),
                ('words', models.IntegerField(default=2000)),
                ('ebay_access_token', models.TextField(blank=True, default='', verbose_name='Ebay Access Token')),
                ('facebook_user_id', models.TextField(blank=True, default='', verbose_name='Facebook User ID')),
                ('facebook_page_id', models.TextField(blank=True, default='', verbose_name='Facebook Page ID')),
                ('instagram_user_id', models.TextField(blank=True, default='', verbose_name='Instagram User ID')),
                ('facebook_access_token', models.TextField(blank=True, default='', verbose_name='Facebook Access Token')),
                ('store_type', models.CharField(choices=[('none', 'None'), ('woocommerce', 'WooCommerce'), ('shopify', 'Shopify')], default='none', max_length=20)),
                ('store_name', models.TextField(blank=True, default='', verbose_name='Store name')),
                ('woocommerce_store_name', models.TextField(blank=True, default='', verbose_name='WooCommerce store name')),
                ('woocommerce_host', models.TextField(blank=True, default='', verbose_name='WooCommerce store domain')),
                ('woocommerce_consumer_key', models.TextField(blank=True, default='', verbose_name='WooCommerce consumer key')),
                ('woocommerce_secret_key', models.TextField(blank=True, default='', verbose_name='WooCommerce secret key')),
                ('shopify_store_name', models.TextField(blank=True, default='', verbose_name='Shopify store name')),
                ('shopify_host', models.TextField(blank=True, default='', verbose_name='Shopify store domain')),
                ('shopify_consumer_key', models.TextField(blank=True, default='', verbose_name='Shopify consumer key')),
                ('shopify_secret_key', models.TextField(blank=True, default='', verbose_name='Shopify secret key')),
                ('cjdropshipping_email', models.TextField(blank=True, default='', verbose_name='CJDropshipping Email')),
                ('cjdropshipping_api_key', models.TextField(blank=True, default='', verbose_name='CJDropshipping API Key')),
                ('description', models.TextField(blank=True, default='', max_length=600, verbose_name='Description')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_info', models.TextField(blank=True, default='', max_length=10000, verbose_name='Full JSON response:')),
                ('shipping_zip', models.CharField(blank=True, default='', max_length=10, verbose_name='Shipping Zip')),
                ('shipping_country_code', models.CharField(blank=True, default='', max_length=10, verbose_name='Shipping Country Code')),
                ('shipping_country', models.CharField(blank=True, default='', max_length=100, verbose_name='Shipping Country')),
                ('shipping_province', models.CharField(blank=True, default='', max_length=100, verbose_name='Shipping Province')),
                ('shipping_city', models.CharField(blank=True, default='', max_length=100, verbose_name='Shipping City')),
                ('shipping_address', models.TextField(blank=True, default='', max_length=500, verbose_name='Shipping Address')),
                ('shipping_customer_name', models.CharField(blank=True, default='', max_length=100, verbose_name='Shipping Customer Name')),
                ('shipping_phone', models.CharField(blank=True, default='', max_length=20, verbose_name='Shipping Phone')),
                ('remark', models.TextField(blank=True, default='', max_length=500, verbose_name='Remark')),
                ('from_country_code', models.CharField(blank=True, default='', max_length=10, verbose_name='From Country Code')),
                ('logistic_name', models.CharField(blank=True, default='', max_length=100, verbose_name='Logistic Name')),
                ('products', models.TextField(blank=True, default='', max_length=1000, verbose_name='Products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
