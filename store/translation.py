from modeltranslation.translator import register, TranslationOptions
from store.models import Product,  ReviewRating

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'description', 'slug')

@register(ReviewRating)
class ReviewRatingTranslationOptions(TranslationOptions):
    fields = ()