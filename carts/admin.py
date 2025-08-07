from django.contrib import admin
from .models import Cart, CartItem
from modeltranslation.admin import TranslationAdmin
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')

class CartItemAdmin(TranslationAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
