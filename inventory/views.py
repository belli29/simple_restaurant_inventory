from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, TemplateView
from django.db.models import Sum, F
from .models import Ingredient, MenuItem, Purchase, RecipeRequirements

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


class PurchaseListView(ListView):
    model = Purchase
    template_name = 'inventory/purchases.html'
    context_object_name = 'purchases'


class ProfitRevenueView(TemplateView):
    template_name = 'inventory/profit_revenue.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculate total revenue
        total_revenue = (
            Purchase.objects.annotate(total_price=Sum(F('items__price')))
            .aggregate(total_revenue=Sum('total_price'))['total_revenue']
        )
        # Calculate total cost
        total_cost = sum(
            sum(ingredient['ingredient__unit_price'] * ingredient['quantity'] for ingredient 
                in RecipeRequirements.objects.filter(menu_item=item).values('ingredient__unit_price', 'quantity'))
            for item in MenuItem.objects.all()
        )
        # Calculate profit
        profit = total_revenue - total_cost
        context['total_revenue'] = total_revenue
        context['total_cost'] = total_cost
        context['profit'] = profit
        return context

