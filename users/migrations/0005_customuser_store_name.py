# Generated by Django 3.2.3 on 2023-04-14 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20230414_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='store_name',
            field=models.TextField(blank=True, default='', verbose_name='Store name'),
        ),
    ]