from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.urls import reverse


from .models import Category, Product
from .views import product_list


class TestCategoriesModel(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        category = self.category
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(str(category), 'django')

    def test_category_url(self):
        category = self.category
        response = self.client.post(reverse('product:category_list', args=[category.slug]))
        self.assertEqual(response.status_code, 200)


class TestProductModel(TestCase):
    def setUp(self):
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        self.product1 = Product.objects.create(category_id=1, title='django beginners', created='admin', slug='django-beginners', price='20.00', image='django.png')
        self.product2 = Product.objects.create(category_id=1, title='django advanced', created='admin', slug='django-advanced', price='20.00', image='django.png')

    def test_product_model_entry(self):
        product = self.product
        self.assertTrue(isinstance(product, Product))
        self.assertEqual(str(product), 'django beginners')

class TestViewResponses(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        User.objects.create(username='admin')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(category_id=1, title='django beginners', created='admin', slug='django-beginners', price='20.00', image='django.png')

    def test_url_allowed_hosts(self):
        response = self.client.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.client.get('/', HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        response = product_list(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Home</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        request = self.factory.get('products/django-beginners')
        response = product_list(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Home</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
