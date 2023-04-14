# Generated by Django 3.2.3 on 2023-04-14 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_words'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='cjdropshipping_api_key',
            field=models.TextField(blank=True, default='', verbose_name='CJDropshipping API Key'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='cjdropshipping_email',
            field=models.TextField(blank=True, default='', verbose_name='CJDropshipping Email'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='store_type',
            field=models.CharField(choices=[('none', 'None'), ('woocommerce', 'WooCommerce'), ('shopify', 'Shopify')], default='none', max_length=20),
        ),
    ]
