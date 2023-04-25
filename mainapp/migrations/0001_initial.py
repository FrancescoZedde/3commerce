# Generated by Django 3.2.3 on 2023-04-25 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.TextField()),
                ('itemName', models.TextField()),
                ('description', models.TextField()),
                ('descriptionTemplate', models.TextField()),
                ('descriptionFeatures', models.TextField()),
                ('descriptionChatGpt', models.TextField()),
                ('supplierSellPrice', models.TextField()),
                ('sellPrice', models.TextField()),
                ('supplier', models.TextField()),
                ('supplierSku', models.TextField()),
                ('brand', models.TextField(blank=True)),
                ('woocommerceId', models.TextField()),
                ('categoryFirst', models.TextField()),
                ('categorySecond', models.TextField()),
                ('categoryThird', models.TextField()),
                ('categoryFourth', models.TextField()),
                ('attributes', models.TextField()),
                ('productWeight', models.TextField()),
                ('productType', models.TextField()),
                ('entryNameEn', models.TextField()),
                ('materialNameEn', models.TextField()),
                ('packingWeight', models.TextField()),
                ('productImage', models.TextField()),
                ('productImageSet', models.TextField()),
                ('jsonDataImported', models.TextField()),
                ('jsonVariants', models.TextField()),
                ('jsonWooCommerceExport', models.TextField()),
                ('jsonWooCommerceExportVariants', models.TextField()),
                ('jsonEbayExportCreateInventoryItems', models.TextField()),
                ('jsonEbayExportCreateItemsGroup', models.TextField()),
                ('jsonEbayExportCreateOffers', models.TextField()),
                ('onsaleWoocommerce', models.BooleanField(default=False)),
                ('onsaleEbay', models.BooleanField(default=False)),
                ('outOfStock', models.BooleanField(default=False)),
                ('ebayCategory', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WoocommerceStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('url', models.CharField(max_length=155)),
                ('ck', models.CharField(max_length=155)),
                ('cs', models.CharField(max_length=155)),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variantSku', models.TextField()),
                ('vid', models.TextField()),
                ('variantNameEn', models.TextField(null=True)),
                ('description', models.TextField()),
                ('supplierSellPrice', models.FloatField()),
                ('sellPrice', models.FloatField()),
                ('supplier', models.TextField()),
                ('supplierSku', models.TextField()),
                ('variantImage', models.TextField()),
                ('variantKey', models.TextField()),
                ('variantLength', models.TextField()),
                ('variantWidth', models.TextField()),
                ('variantHeight', models.TextField()),
                ('variantVolume', models.TextField()),
                ('variantWeight', models.TextField()),
                ('areaId', models.TextField()),
                ('storageNum', models.TextField()),
                ('countryCode', models.TextField()),
                ('allLocations', models.TextField()),
                ('firstShippingMethod', models.TextField()),
                ('secondShippingMethod', models.TextField()),
                ('thirdShippingMethod', models.TextField()),
                ('allShippingMethods', models.TextField()),
                ('onsaleWoocommerce', models.BooleanField(default=False)),
                ('onsaleEbay', models.BooleanField(default=False)),
                ('outOfStock', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant', to='mainapp.inventoryitem')),
            ],
        ),
    ]
