from django.contrib import admin
from .models import Category
from modeltranslation.admin import TranslationAdmin
# Register your models here.

class CategoryAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug', 'description')

admin.site.register(Category, CategoryAdmin)
