from django.db import models
from django.contrib.auth.models import User

class CartItem(models.Model):
    username = models.CharField(max_length=150)
    product_id = models.PositiveIntegerField()
    quantity = models.DecimalField(default=1.00,decimal_places=2,max_digits=10)

    def __str__(self):
        return f"{self.username} - {self.product_id}"

class MetaCart(models.Model):
    user = models.CharField(max_length=150)
    items = models.PositiveIntegerField(default=0)
    amount = models.DecimalField(default=0.00,decimal_places=2,max_digits=20)
    charges = models.DecimalField(default=0.00,decimal_places=2,max_digits=20)
    total = models.DecimalField(default=0.00,decimal_places=2,max_digits=20)
    discount = models.DecimalField(default=0.00,decimal_places=2,max_digits=20)
    net = models.DecimalField(default=0.00,decimal_places=2,max_digits=20)
    
    def __str__(self) -> str:
        return self.user
    
