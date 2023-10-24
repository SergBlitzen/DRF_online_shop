from django.core.exceptions import ValidationError
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='categories/')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='subcategories/')
    category = models.ForeignKey(
        Category, related_name='subcategories', on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    price = models.FloatField()
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    subcategory = models.ForeignKey(
        SubCategory, related_name='products', on_delete=models.SET_NULL,
        null=True, blank=True,
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.category is None and self.subcategory is None:
            raise ValidationError(
                "У продукта должна быть категория или подкатегория."
            )


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продукта"
        ordering = ['id']


class Cart(models.Model):
    user = models.OneToOneField(
        User, related_name='cart', on_delete=models.CASCADE, unique=True
    )
    products = models.ManyToManyField(
        Product,
        through='ProductCart',
        through_fields=('cart', 'product')
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина пользователя: {self.user.username}"


class ProductCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Продукт в корзине"
        verbose_name_plural = "Продукты в корзине"
        constraints = [
            models.UniqueConstraint(
                fields=('cart', 'product'),
                name='unique_cart_product'
            )
        ]

    def __str__(self):
        return (f"Продукт {self.product.name} "
                f" в корзине пользователя {self.cart.user.username}")
