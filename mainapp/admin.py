from django.contrib import admin

# Register your models here.
from mainapp.models import InventoryItem, Variant, WoocommerceStore
# Register your models here.

admin.site.register(InventoryItem)
admin.site.register(Variant)
admin.site.register(WoocommerceStore)