from django import forms
from .models import Ingredient

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