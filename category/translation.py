from modeltranslation.translator import register, TranslationOptions
from category.models import Category

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name', 'description') 
