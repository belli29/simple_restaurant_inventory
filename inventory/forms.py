from django import forms
from .models import Ingredient, Purchase, MenuItem, PurchaseItem, RecipeRequirements

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit_price', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_name', 'required': 'required'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_quantity', 'required': 'required'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_unit_price', 'required': 'required'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_unit', 'required': 'required'}),
        }

class RecipeRequirementsForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirements
        fields = ['menu_item', 'ingredient', 'quantity']
        widgets = {
            'menu_item': forms.Select(attrs={'class': 'form-control'}),
            'ingredient': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_quantity', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ingredient'].queryset = Ingredient.objects.all()
        self.fields['ingredient'].label_from_instance = lambda obj: f"{obj.name} ({obj.unit})"

    def save(self, commit=True):
        menu_item = self.cleaned_data.get('menu_item')
        ingredient = self.cleaned_data.get('ingredient')
        quantity = self.cleaned_data.get('quantity')
        recipe_requirement, created = RecipeRequirements.objects.update_or_create(
            menu_item=menu_item,
            ingredient=ingredient,
            defaults={'quantity': quantity}
        )

        return recipe_requirement

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['menu_item', 'quantity']
        widgets = {
            'menu_item': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = []

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['title', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
        }