from rest_framework import serializers

from shop.models import (
    Category, SubCategory, Product,
    ProductImage, Cart, ProductCart,
)


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    slug = serializers.SlugField()
    image = serializers.ImageField()

    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    slug = serializers.SlugField()
    image = serializers.ImageField()
    category = CategorySerializer()

    class Meta:
        model = SubCategory
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    slug = serializers.SlugField()
    category = CategorySerializer()
    subcategory = SubCategorySerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    """
    Сериализатор вывода продукта в корзине.
    """

    class Meta:
        model = Product
        fields = ('name', 'price')


class ProductCartSerializer(serializers.ModelSerializer):
    """
    Сериализатор вывода количества продукта в корзине.
    """
    quantity = serializers.IntegerField()
    product = ProductListSerializer()

    class Meta:
        model = ProductCart
        fields = ('product', 'quantity')


class CartSerializer(serializers.ModelSerializer):
    products = ProductCartSerializer(many=True, source='productcart_set')
    full_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('products', 'full_price')

    def get_full_price(self, value):
        """
        Возвращает цену всей корзины по формуле
        (товар * количество) + (товар * количество)...
        """
        products = ProductCart.objects.filter(cart=value)
        products_list = []
        for product_cart_obj in products:
            product = product_cart_obj.product
            product_price = product.price * product_cart_obj.quantity
            products_list.append(product_price)
        return sum(products_list)
