from django.test import TestCase
from django.urls import reverse
from .models import Ingredient, MenuItem, RecipeRequirements

class IngredientTests(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Tomato", quantity=100, unit_price=0.5, unit="kg")

    def test_ingredient_creation(self):
        self.assertEqual(self.ingredient.name, "Tomato")
        self.assertEqual(self.ingredient.quantity, 100)
        self.assertEqual(self.ingredient.unit_price, 0.5)
        self.assertEqual(self.ingredient.unit, "kg")

    def test_add_ingredient_view(self):
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

class MenuItemTests(TestCase):
    def setUp(self):
        self.menu_item = MenuItem.objects.create(title="Pizza", price=10.0)

    def test_menu_item_creation(self):
        self.assertEqual(self.menu_item.title, "Pizza")
        self.assertEqual(self.menu_item.price, 10.0)

    def test_add_menu_item_view(self):
        response = self.client.get(reverse('add_menu_item'))
        self.assertEqual(response.status_code, 200)

    def test_add_menu_item_form(self):
        response = self.client.post(reverse('add_menu_item'), {
            'title': 'Burger',
            'price': 8.0
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MenuItem.objects.filter(title='Burger').exists())

    def test_add_menu_item_template(self):
        response = self.client.get(reverse('add_menu_item'))
        self.assertTemplateUsed(response, 'inventory/add_menu_item.html')

class RecipeRequirementsTests(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Tomato", quantity=100, unit_price=0.5, unit="kg")
        self.menu_item = MenuItem.objects.create(title="Pizza", price=10.0)
        self.recipe_requirement = RecipeRequirements.objects.create(menu_item=self.menu_item, ingredient=self.ingredient, quantity=2.0)

    def test_recipe_requirement_creation(self):
        self.assertEqual(self.recipe_requirement.menu_item, self.menu_item)
        self.assertEqual(self.recipe_requirement.ingredient, self.ingredient)
        self.assertEqual(self.recipe_requirement.quantity, 2.0)

    def test_add_recipe_requirement_view(self):
        response = self.client.get(reverse('add_recipe_requirement'))
        self.assertEqual(response.status_code, 200)

    def test_add_recipe_requirement_form(self):
        response = self.client.post(reverse('add_recipe_requirement'), {
            'menu_item': self.menu_item.id,
            'ingredient': self.ingredient.id,
            'quantity': 3.0
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(RecipeRequirements.objects.filter(menu_item=self.menu_item, ingredient=self.ingredient, quantity=3.0).exists())

    def test_add_recipe_requirement_template(self):
        response = self.client.get(reverse('add_recipe_requirement'))
        self.assertTemplateUsed(response, 'inventory/add_recipe_requirement.html')
