from django.contrib import admin
from .models import CustomUser, CheckoutSession, ContractOrder
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(CheckoutSession)
admin.site.register(ContractOrder)
