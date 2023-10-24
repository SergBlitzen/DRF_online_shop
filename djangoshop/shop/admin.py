from django.contrib import admin

from .models import (
    Category, SubCategory, Product, ProductImage,
    Cart, ProductCart,
)


class ImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    max_num = 3


class ProductCartInline(admin.StackedInline):
    model = ProductCart
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    ...


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [ProductCartInline]


@admin.register(ProductCart)
class ProductCartAdmin(admin.ModelAdmin):
    ...
