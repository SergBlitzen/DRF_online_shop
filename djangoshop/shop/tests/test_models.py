import tempfile
import shutil

from django.conf import settings
from django.db import IntegrityError, transaction
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from shop.models import (
    Product, ProductCart, ProductImage,
    Cart, Category, SubCategory,
)
from users.models import User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CategoryTestCase(TestCase):

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

    def test_category_object_exists(self):
        """Проверка доступа к объекту модели."""
        categories_count = Category.objects.count()
        expected_count = 1
        self.assertEqual(categories_count, expected_count)

    def test_category_object_have_correct_data(self):
        """Проверка корректного вывода данных модели."""
        category = Category.objects.all()[0]
        expected_data = {
            'name': 'test_category_1',
            'slug': 'testcat1',
        }
        for field, value in expected_data.items():
            with self.subTest(field=field, value=value):
                self.assertEqual(
                    getattr(category, field),
                    expected_data[field]
                )

    def test_cannot_duplicate_slug(self):
        """Проверка невозможности создать категорию
        с существующим слагом."""
        with transaction.atomic():
            try:
                Category.objects.create(
                    name='test_category_2',
                    slug='testcat1',
                )
            except Exception as e:
                self.assertEqual(type(e), IntegrityError)
        categories_count = Category.objects.count()
        expected_count = 1
        self.assertEqual(categories_count, expected_count)

    def test_access_subcategory(self):
        """Проверка доступа к подкатегории через категорию."""
        cls_subcategory = CategoryTestCase.subcat_1
        model_subcategory = CategoryTestCase.cat_1.subcategories.all()[0]
        self.assertEqual(cls_subcategory, model_subcategory)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)


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

    def test_subcategory_object_exists(self):
        """Проверка доступа к объекту модели."""
        subcategories_count = SubCategory.objects.count()
        expected_count = 1
        self.assertEqual(subcategories_count, expected_count)

    def test_subcategory_object_have_correct_data(self):
        """Проверка корректного вывода данных модели."""
        subcategory = SubCategory.objects.all()[0]
        expected_data = {
            'name': 'test_subcategory_1',
            'slug': 'testsubcat1',
            'category': SubCategoryTestCase.cat_1,
        }
        for field, value in expected_data.items():
            with self.subTest(field=field, value=value):
                self.assertEqual(
                    getattr(subcategory, field),
                    expected_data[field]
                )

    def test_cannot_duplicate_slug(self):
        """Проверка невозможности создать подкатегорию
        с существующим слагом."""
        with transaction.atomic():
            try:
                SubCategory.objects.create(
                    name='test_subcategory_2',
                    slug='testsubcat1',
                    category=SubCategoryTestCase.cat_1,
                )
            except Exception as e:
                self.assertEqual(type(e), IntegrityError)
        categories_count = SubCategory.objects.count()
        expected_count = 1
        self.assertEqual(categories_count, expected_count)

    def test_access_subcategory(self):
        """Проверка доступа к категории через подкатегорию."""
        cls_category = CategoryTestCase.cat_1
        model_category = Category.objects.get(
            subcategories__name='test_subcategory_1'
        )
        self.assertEqual(cls_category, model_category)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ProductTestCase(TestCase):

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
        cls.product_2 = Product.objects.create(
            name='test_product_2',
            slug='testprod2',
            price=1234,
            subcategory=cls.subcat_1,
        )
        cls.product_2_image = ProductImage.objects.create(
            image=cls.test_image,
            product=cls.product_2,
        )
        cls.product_3 = Product.objects.create(
            name='test_product_3',
            slug='testprod3',
            price=12345,
            category=cls.cat_1,
            subcategory=cls.subcat_1,
        )
        cls.product_3_image = ProductImage.objects.create(
            image=cls.test_image,
            product=cls.product_3,
        )

    def test_products_exist(self):
        """Проверка доступа к объекту модели."""
        products = Product.objects.count()
        expected_count = 3
        self.assertEqual(products, expected_count)

    def test_product_have_correct_data(self):
        """Проверка корректного вывода данных объекта."""
        product = Product.objects.all()[0]
        expected_data = {
            'name': 'test_product_1',
            'slug': 'testprod1',
            'category': ProductTestCase.cat_1,
        }
        for field, value in expected_data.items():
            with self.subTest(field=field, value=value):
                self.assertEqual(
                    getattr(product, field),
                    expected_data[field]
                )

    def test_cannot_duplicate_product_slug(self):
        """Проверка невозможности создать объект
        с уже существующим слагом."""
        with transaction.atomic():
            try:
                Product.objects.create(
                    name='test_product_4',
                    slug='testprod1',
                    category=ProductTestCase.cat_1,
                )
            except Exception as e:
                self.assertEqual(type(e), IntegrityError)
        products_count = Product.objects.count()
        expected_count = 3
        self.assertEqual(products_count, expected_count)

    def test_cannot_add_product_without_categories(self):
        """Проверка невозможности создать объект продукта
        без указания категории или подкатегории."""
        with transaction.atomic():
            try:
                Product.objects.create(
                    name='test_product_4',
                    slug='testprod4',
                )
            except Exception as e:
                self.assertEqual(type(e), IntegrityError)
        products_count = Product.objects.count()
        expected_count = 3
        self.assertEqual(products_count, expected_count)

    def test_add_another_product(self):
        """Проверка корректного создания нового объекта."""
        new_product = Product.objects.create(
            name='test_product_4',
            slug='testprod4',
            price=123456,
            category=ProductTestCase.cat_1,
        )
        products_count = Product.objects.count()
        expected_count = 4
        self.assertEqual(products_count, expected_count)
        ProductImage.objects.create(
            image=ProductTestCase.test_image,
            product=new_product,
        )
        product_images_count = ProductImage.objects.count()
        expected_count = 4
        self.assertEqual(product_images_count, expected_count)

    def test_access_product_images(self):
        """Проверка доступа к изображениям продукта."""
        product = Product.objects.all()[0]
        product_image = product.images.all()[0]
        image = ProductImage.objects.all()[0]
        self.assertEqual(product_image, image)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CartTestCase(TestCase):

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

    def test_cart_object_exists(self):
        """Проверка доступа к объекту модели."""
        carts_count = Cart.objects.count()
        expected_count = 1
        self.assertEqual(carts_count, expected_count)

    def test_cart_object_have_correct_data(self):
        """Проверка корректного вывода данных объекта."""
        cart_user = CartTestCase.cart.user
        expected_data = User.objects.all()[0]
        self.assertEqual(cart_user, expected_data)

    def test_product_cart_object_exists(self):
        """Проверка доступа к объекту модели."""
        product_cart_count = Cart.objects.count()
        expected_count = 1
        self.assertEqual(product_cart_count, expected_count)

    def test_product_cart_object_have_correct_data(self):
        """Проверка корректного вывода данных объекта."""
        product_cart = CartTestCase.product_1_cart
        cart = Cart.objects.all()[0]
        product = Product.objects.all()[0]
        expected_data = {
            'cart': cart,
            'product': product,
            'quantity': 10
        }
        for field, value in expected_data.items():
            with self.subTest(field=field, value=value):
                self.assertEqual(
                    getattr(product_cart, field),
                    expected_data[field]
                )

    def test_cannot_add_duplicate_product_carts(self):
        """Проверка невозможности создать несколько
        объектов с одинаковым продуктом."""
        with transaction.atomic():
            try:
                ProductCart.objects.create(
                    cart=CartTestCase.cart,
                    product=CartTestCase.product_1,
                    quantity=1,
                )
            except Exception as e:
                self.assertEqual(type(e), IntegrityError)
        products_cart_count = ProductCart.objects.count()
        expected_count = 1
        self.assertEqual(products_cart_count, expected_count)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
