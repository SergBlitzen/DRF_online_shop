from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views.shop_views import (
    CategoryViewSet, SubCategoryViewSet,
    ProductViewSet, CartView,
)


router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('subcategories', SubCategoryViewSet)
router.register('products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', CartView.as_view())
]
