from modeltranslation.translator import register, TranslationOptions
from accounts.models import Account, UserProfile
from carts.models import CartItem
from category.models import Category
from orders.models import Payment, Order
from store.models import Product,  ReviewRating


@register(Payment)
class PaymentTranslationOptions(TranslationOptions):
    fields = ('payment_method', 'status') 

@register(Order)
class OrderTranslationOptions(TranslationOptions):
    fields = (
        'first_name', 'last_name', 'address_line_1', 'address_line_2',
        'country', 'state', 'city', 'order_note', 'status'
    ) 
