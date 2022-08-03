from django.contrib import admin
from django.contrib.admin import register

from category.models import Category, CategoryImage


class CategoryImageAdmin(admin.TabularInline):
    model = CategoryImage
    extra = 2


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug']
    inlines = [CategoryImageAdmin]





