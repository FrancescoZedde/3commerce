# Generated by Django 3.2.3 on 2023-04-17 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_order_vids'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='external_order_id',
            field=models.TextField(blank=True, default='', max_length=10000, verbose_name='External order id:'),
        ),
    ]