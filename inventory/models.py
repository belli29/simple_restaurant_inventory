from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    quantity = models.IntegerField(blank=False, null=False)
    unit_price = models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)
    unit = models.CharField(max_length=100, null=False, blank=False)
    
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)

    def __str__(self):
        return self.title

class RecipeRequirements(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)

class Purchase(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(MenuItem, through='PurchaseItem')

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='purchase_items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
