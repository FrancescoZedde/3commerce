# Generated by Django 3.2.3 on 2023-03-14 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='shopify_consumer_key',
            field=models.TextField(blank=True, default='', verbose_name='Shopify consumer key'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='shopify_host',
            field=models.TextField(blank=True, default='', verbose_name='Shopify store domain'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='shopify_secret_key',
            field=models.TextField(blank=True, default='', verbose_name='Shopify secret key'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='shopify_store_name',
            field=models.TextField(blank=True, default='', verbose_name='Shopify store name'),
        ),
    ]
