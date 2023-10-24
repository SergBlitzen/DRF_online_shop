from rest_framework import viewsets, views, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop.models import Category, SubCategory, Product, Cart, ProductCart
from api.serializers.shop_serializers import (
    CategorySerializer, SubCategorySerializer,
    ProductSerializer, ProductCartSerializer,
    CartSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(methods=['post'], detail=True, url_path='cart',
            permission_classes=[IsAuthenticated])
    def add_to_cart(self, request, pk=None):
        """
        Кастомный action для управления корзиной с методами POST, PATCH
        и DELETE. При нескольких POST-запросах на одинаковый продукт
        складывает количества.
        """

        quantity = request.data.get('quantity')
        if not quantity and not isinstance(quantity, int):
            return Response(
                data={"error": "Не указано количество продукта"
                               " или формат ввода неверный."},
                status=status.HTTP_400_BAD_REQUEST
            )
        product = self.get_object()
        if Cart.objects.filter(user=request.user):
            cart = request.user.cart
        else:
            cart = Cart.objects.create(user=request.user)
        if obj_list := ProductCart.objects.filter(product=product, cart=cart):
            obj = obj_list[0]
            obj.quantity += int(quantity)
            obj.save()
        else:
            obj = ProductCart.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
            )
        try:
            serializer = ProductCartSerializer(obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            obj.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @add_to_cart.mapping.patch
    def update_product_quantity(self, request, pk=None):
        """
        PATCH-метод управления продуктом в корзине, полностью заменяет
        количество на указанное в теле запроса.
        """

        quantity = request.data.get('quantity')
        if not quantity and not isinstance(quantity, int):
            return Response(
                data={"error": "Не указано количество продукта"
                               " или формат ввода неверный."},
                status=status.HTTP_400_BAD_REQUEST
            )
        product = self.get_object()
        cart = request.user.cart
        if obj := ProductCart.objects.filter(product=product, cart=cart)[0]:
            obj.quantity = quantity
            obj.save()
            serializer = ProductCartSerializer(obj)
            return Response(
                serializer.data, status=status.HTTP_206_PARTIAL_CONTENT
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @add_to_cart.mapping.delete
    def delete_from_cart(self, request, pk=None):
        """
        Удаляет продукт из корзины со всем количеством.
        """

        product = self.get_object()
        cart = request.user.cart
        try:
            if obj := ProductCart.objects.filter(
                    product=product, cart=cart
            )[0]:
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CartView(views.APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        if cart := Cart.objects.filter(user=request.user):
            serializer = CartSerializer(cart[0])
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            cart = Cart.objects.create(user=request.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        if cart := Cart.objects.filter(user=request.user)[0]:
            for product in ProductCart.objects.filter(cart=cart):
                product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
