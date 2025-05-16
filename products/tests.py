from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Product


class CategoryModelTest(TestCase):
    def test_category_creation(self):
        """Testeamos que se puede crear una categoría y se asigna el nombre correctamente"""
        category = Category.objects.create(name="Electronics")
        self.assertEqual(category.name, "Electronics")
        self.assertEqual(str(category), "Electronics")


class ProductViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_product_list_view_status_code(self):
        """Testeamos que al llamar la vista de listado de productos se obtiene un código de estado 200 (OK)"""
        url = reverse('product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_list_view_uses_correct_template(self):
        """Testeamos que la vista esté usando la template correcta"""
        url = reverse('product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')
