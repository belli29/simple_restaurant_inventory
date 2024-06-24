from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    quantity = models.IntegerField(blank=False, null=False)
    unit_price = models.DecimalField(decimal_places=2, max_digits=3, blank=False, null=False)
    unit = models.CharField(max_length=100, null=False, blank=False)

class MenuItem(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=3, blank=False, null=False)

class RecipeRequirements(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)
    

class Purchase(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(MenuItem)
    
    def calculate_total_cost(self):
        total_cost = sum(item.price for item in self.items.all())
        return total_cost

    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost()
        super().save(*args, **kwargs)
    


    
    
