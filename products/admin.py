from django.contrib import admin

from .models import Category, Product, Review


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    fieldsets = (
        ('', {
            'fields': ['name', 'slug']
        }),
        ('Optional', {
            'fields': ['description'],
            'description': 'These fields are Optional.',
            'classes': ('collapse',),
        }),
    )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'vendor', 'created', 'is_approved']
    list_editable = ['is_approved']
    list_filter = ['is_available', 'created', 'updated', 'is_approved']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ReviewInline]
