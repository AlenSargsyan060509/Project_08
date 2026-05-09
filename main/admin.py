from django.contrib import admin
from .models import Category, Product

# Способ через декоратор (более современный)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price']
    list_filter = ['category']