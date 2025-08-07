from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery
import admin_thumbnails
from modeltranslation.admin import TranslationAdmin


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(TranslationAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')

class ReviewRatingAdmin(TranslationAdmin):  # Используйте TranslationAdmin
    list_display = ('subject', 'review', 'rating', 'user', 'product', 'created_at', 'updated_at', 'status')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(ProductGallery)
