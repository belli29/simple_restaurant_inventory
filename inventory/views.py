from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, TemplateView, CreateView
from django.db.models import Sum, F
from .models import Ingredient, MenuItem, Purchase, RecipeRequirements, PurchaseItem
from .forms import IngredientForm, PurchaseForm, PurchaseItemForm, MenuItemForm, RecipeRequirementsForm
from django.forms import inlineformset_factory

class HomeView(TemplateView):
    template_name = 'inventory/home.html'

class IngredientListView(ListView):
    model = Ingredient
    template_name = 'inventory/index.html'
    context_object_name = 'ingredients'

class IngredientDeleteView(DeleteView):
    model = Ingredient
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class MenuItemListView(ListView):
    model = MenuItem
    template_name = 'inventory/menu.html'
    context_object_name = 'menu_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_items = context['menu_items']
        for item in menu_items:
            item.ingredients = RecipeRequirements.objects.filter(menu_item=item)
        return context


class PurchaseListView(ListView):
    model = Purchase
    template_name = 'inventory/purchases.html'
    context_object_name = 'purchases'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchases = context['purchases']
        for purchase in purchases:
            total_price = sum(item.menu_item.price * item.quantity for item in purchase.purchase_items.all())
            purchase.total_price = total_price
        return context


class ProfitRevenueView(TemplateView):
    template_name = 'inventory/profit_revenue.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate total revenue
        total_revenue = (
            Purchase.objects.annotate(total_price=Sum(F('purchase_items__menu_item__price') * F('purchase_items__quantity')))
            .aggregate(total_revenue=Sum('total_price'))['total_revenue']
        )
        
        # Calculate total cost
        total_cost = 0
        menu_items = MenuItem.objects.all()
        
        for item in menu_items:
            item_cost = 0
            ingredients = RecipeRequirements.objects.filter(menu_item=item).values('ingredient__unit_price', 'quantity')
            
            for ingredient in ingredients:
                ingredient_cost = ingredient['ingredient__unit_price'] * ingredient['quantity']
                item_cost += ingredient_cost
            
            total_cost += item_cost

        profit = total_revenue - total_cost
        total_revenue = round(total_revenue, 2)
        total_cost = round(total_cost, 2)
        profit = round(profit, 2)

        context['total_revenue'] = total_revenue
        context['total_cost'] = total_cost
        context['profit'] = profit
        return context

class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'inventory/add_ingredient.html'
    success_url = reverse_lazy('index')

class RecipeRequirementsCreateView(CreateView):
    model = RecipeRequirements
    form_class = RecipeRequirementsForm
    template_name = 'inventory/add_recipe_requirement.html'
    success_url = reverse_lazy('menu')

class PurchaseCreateView(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'inventory/add_purchase.html'
    success_url = reverse_lazy('purchases')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        PurchaseItemFormSet = inlineformset_factory(Purchase, PurchaseItem, form=PurchaseItemForm, extra=1)
        if self.request.POST:
            data['purchase_items'] = PurchaseItemFormSet(self.request.POST)
        else:
            data['purchase_items'] = PurchaseItemFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        purchase_items = context['purchase_items']
        self.object = form.save()
        if purchase_items.is_valid():
            purchase_items.instance = self.object
            purchase_items.save()
        return super().form_valid(form)

class MenuItemCreateView(CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'inventory/add_menu_item.html'
    success_url = reverse_lazy('menu')



