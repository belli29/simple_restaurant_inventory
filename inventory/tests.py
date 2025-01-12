from django.test import TestCase
from django.urls import reverse
from .models import Ingredient

class IngredientCreateViewTests(TestCase):
    def test_add_ingredient_page_status_code(self):
        response = self.client.get(reverse('add_ingredient'))
        self.assertEqual(response.status_code, 200)

    def test_add_ingredient_form(self):
        response = self.client.post(reverse('add_ingredient'), {
            'name': 'Tomato',
            'quantity': 10,
            'unit_price': 1.50,
            'unit': 'kg'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(name='Tomato').exists())

    def test_add_ingredient_template(self):
        response = self.client.get(reverse('add_ingredient'))
        self.assertTemplateUsed(response, 'inventory/add_ingredient.html')
