import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from shop.models import (
    Product, ProductCart, ProductImage,
    Cart, Category, SubCategory,
)
from users.models import User


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ShopUrlsTestCase(TestCase):

    test_image_bytes = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    test_image = SimpleUploadedFile(
        'test_image.gif',
        test_image_bytes,
        content_type='image/gif'
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cat_1 = Category.objects.create(
            name='test_category_1',
            slug='testcat1',
            image=cls.test_image,
        )
        cls.subcat_1 = SubCategory.objects.create(
            name='test_subcategory_1',
            slug='testsubcat1',
            image=cls.test_image,
            category=cls.cat_1,
        )
        cls.product_1 = Product.objects.create(
            name='test_product_1',
            slug='testprod1',
            price=123,
            category=cls.cat_1,
        )
        cls.product_1_image = ProductImage.objects.create(
            image=cls.test_image,
            product=cls.product_1,
        )
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword1',
        )
        cls.cart = Cart.objects.create(
            user=cls.user,
        )
        cls.product_1_cart = ProductCart.objects.create(
            cart=cls.cart,
            product=cls.product_1,
            quantity=10,
        )

    def setUp(self):
        super().setUp()
        self.anon_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(
            ShopUrlsTestCase.user
        )

    def test_anonymous_user_get_urls(self):
        """Проверка доступа неавторизованного пользователя."""
        urls_get_statuses = {
            '/api/v1/categories/': HTTPStatus.OK,
            '/api/v1/subcategories/': HTTPStatus.OK,
            '/api/v1/products/': HTTPStatus.OK,
            '/api/v1/products/1/': HTTPStatus.OK,
            '/api/v1/cart/': HTTPStatus.UNAUTHORIZED,
        }
        for url, status_code in urls_get_statuses.items():
            with self.subTest(url=url, status=status_code):
                response = self.anon_client.get(url)
                self.assertEqual(response.status_code, status_code)

    def test_authorized_user_post_cart_data(self):
        """Проверка доступа авторизованного пользователя
        к возможностям корзины."""
        post_url = '/api/v1/products/1/cart/'
        post_data = {
            'quantity': 10
        }
        post_response = self.anon_client.post(post_url, data=post_data)
        self.assertEqual(post_response.status_code, HTTPStatus.UNAUTHORIZED)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
