from modeltranslation.translator import register, TranslationOptions
from accounts.models import Account, UserProfile
from carts.models import CartItem
from category.models import Category
from orders.models import Payment, Order
from store.models import Product,  ReviewRating


@register(Account)
class AccountTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name')

@register(UserProfile)
class UserProfileTranslationOptions(TranslationOptions):
    fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country')

@register(CartItem)
class CartItemTranslationOptions(TranslationOptions):
    fields = ('product')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name', 'description') 

@register(Payment)
class PaymentTranslationOptions(TranslationOptions):
    fields = ('payment_method', 'status') 

@register(Order)
class OrderTranslationOptions(TranslationOptions):
    fields = (
        'first_name', 'last_name', 'address_line_1', 'address_line_2',
        'country', 'state', 'city', 'order_note', 'status'
    ) 

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'description', 'slug')

@register(ReviewRating)
class ReviewRatingTranslationOptions(TranslationOptions):
    fields = ('subject')