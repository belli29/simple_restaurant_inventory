from django.urls import path
from .views import HomeView, IngredientListView, IngredientDeleteView, MenuItemListView, PurchaseListView, ProfitRevenueView, IngredientCreateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('inventory/', IngredientListView.as_view(), name='index'),
    path('delete/<int:pk>/', IngredientDeleteView.as_view(), name='delete_ingredient'),
    path('menu/', MenuItemListView.as_view(), name='menu'),
    path('purchases/', PurchaseListView.as_view(), name='purchases'),
    path('profit-revenue/', ProfitRevenueView.as_view(), name='profit_revenue'),
    path('add-ingredient/', IngredientCreateView.as_view(), name='add_ingredient'),
]