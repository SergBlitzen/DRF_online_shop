from http import HTTPStatus
import tempfile
import shutil

from django.conf import settings
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework.utils.json import loads, dumps

from shop.models import (
    Product, ProductCart, ProductImage,
    Cart, Category, SubCategory,
)
from users.models import User


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CategoryViewsTest(TestCase):

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
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword1',
        )

    def setUp(self):
        super().setUp()
        self.anon_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(
            CategoryViewsTest.user
        )

    def test_allow_anonymous_access(self):
        """Проверка возможности неавторизованного доступа."""
        address = '/api/v1/categories/'
        response = self.anon_client.get(address)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_allow_authorized_access(self):
        """Проверка возможности авторизованного доступа."""
        address = '/api/v1/categories/'
        response = self.authorized_client.get(address)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_category_in_response(self):
        """Проверка корректного вывода объекта в ответе запроса."""
        address = '/api/v1/categories/'
        response = self.authorized_client.get(address)
        category_data = response.data.get('results')[0]
        expected_cat = CategoryViewsTest.cat_1
        self.assertEqual(category_data.get('name'), expected_cat.name)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def tearDown(self):
        super().tearDown()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class SubCategoryTestCase(TestCase):

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
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword1',
        )

    def setUp(self):
        super().setUp()
        self.anon_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(
            SubCategoryTestCase.user
        )

    def test_allow_anonymous_access(self):
        """Проверка возможности неавторизованного доступа."""
        address = '/api/v1/subcategories/'
        response = self.anon_client.get(address)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_allow_authorized_access(self):
        """Проверка возможности авторизованного доступа."""
        address = '/api/v1/subcategories/'
        response = self.authorized_client.get(address)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_subcategory_in_response(self):
        """Проверка корректного вывода объекта в ответе запроса."""
        address = '/api/v1/subcategories/'
        response = self.authorized_client.get(address)
        subcategory_data = response.data.get('results')[0]
        expected_sub = SubCategoryTestCase.subcat_1
        self.assertEqual(subcategory_data.get('name'), expected_sub.name)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def tearDown(self):
        super().tearDown()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ProductsViewsTestCase(TestCase):

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

    def setUp(self):
        super().setUp()
        self.anon_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(
            ProductsViewsTestCase.user
        )

    def test_allow_anonymous_access(self):
        """Проверка возможности неавторизованного доступа."""
        address = '/api/v1/products/'
        response = self.anon_client.get(address)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_allow_authorized_access(self):
        """Проверка возможности авторизованного доступа."""
        address = '/api/v1/products/'
        response = self.authorized_client.get(address)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_product_in_response(self):
        """Проверка корректного вывода объекта в ответе запроса."""
        address = '/api/v1/products/'
        response = self.authorized_client.get(address)
        product_obj = response.data.get('results')[0]
        expected_product = ProductsViewsTestCase.product_1
        self.assertEqual(product_obj['name'], expected_product.name)

    def test_add_product_to_cart(self):
        """Проверка возможности добавлять продукт в корзину."""
        address = '/api/v1/products/1/cart/'
        data = {
            'quantity': 10
        }
        response = self.authorized_client.post(address, data=data)
        expected_data = {
            "product": {
                "name": "test_product_1",
                "price": 123
            },
            "quantity": 10
        }
        self.assertEqual(response.data, expected_data)
        data = {
            'quantity': 10
        }
        response = self.authorized_client.post(address, data=data)
        expected_data = {
            "product": {
                "name": "test_product_1",
                "price": 123
            },
            "quantity": 20
        }
        self.assertEqual(response.data, expected_data)
        product_cart_count = ProductCart.objects.count()
        expected_count = 1
        self.assertEqual(product_cart_count, expected_count)

    def test_update_product_cart_quantity(self):
        """Проверка возможности изменить количество продуктов в корзине."""
        address = '/api/v1/products/1/cart/'
        data = {
            'quantity': 10
        }
        self.authorized_client.post(address, data=data)
        data = {
            'quantity': 30
        }
        response = self.authorized_client.patch(address, data=data)
        response_quantity = response.data.get('quantity')
        expected_quantity = 30
        self.assertEqual(response_quantity, expected_quantity)

    def test_delete_product_from_cart(self):
        """Проверка возможности удалить продукт из корзины."""
        address = '/api/v1/products/1/cart/'
        data = {
            'quantity': 10
        }
        self.authorized_client.post(address, data=data)
        self.authorized_client.delete(address)
        product_cart_count = ProductCart.objects.count()
        expected_count = 0
        self.assertEqual(product_cart_count, expected_count)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def tearDown(self):
        super().tearDown()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CartViewsTestCase(TestCase):

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
            CartViewsTestCase.user
        )

    def test_deny_anonymous_access(self):
        """Проверка невозможности неавторизованного доступа."""
        address = '/api/v1/cart/'
        response = self.anon_client.get(address)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_allow_authorized_access(self):
        """Проверка возможности авторизованного доступа."""
        address = '/api/v1/cart/'
        response = self.authorized_client.get(address)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_response_have_correct_data(self):
        """Проверка корректного вывода объекта в ответе запроса."""
        address = '/api/v1/cart/'
        response = self.authorized_client.get(address)
        response_data = loads(dumps(response.data))
        expected_data = {
            'products': [
                {
                    'product':
                        {
                            'name': 'test_product_1',
                            'price': 123.0,
                        },
                        'quantity': 10,
                }
            ],
            'full_price': 1230.0
        }
        self.assertEqual(response_data, expected_data)

    def test_flush_cart(self):
        """Проверка возможности полностью очистить корзину."""
        address = '/api/v1/cart/'
        response = self.authorized_client.delete(address)
        response_data = response.data
        expected_response = None
        self.assertEqual(response_data, expected_response)
        product_cart_objects = ProductCart.objects.count()
        expected_count = 0
        self.assertEqual(product_cart_objects, expected_count)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def tearDown(self):
        super().tearDown()
