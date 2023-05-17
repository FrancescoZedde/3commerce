from django.contrib import admin

# Register your models here.
from main_app.models import InventoryItem, Variant, WoocommerceStore

from users_app.models import Order
# Register your models here.

admin.site.register(InventoryItem)
admin.site.register(Variant)
admin.site.register(WoocommerceStore)
admin.site.register(Order)