from django import forms
from .models import Ingredient, Purchase, MenuItem, PurchaseItem

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