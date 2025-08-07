from modeltranslation.translator import register, TranslationOptions
from carts.models import CartItem

@register(CartItem)
class CartItemTranslationOptions(TranslationOptions):
    fields = ('product',) 
