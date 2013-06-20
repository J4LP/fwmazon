from django.db import models

class ShippingDestination(models.Model):
    name = models.CharField(max_length=200)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=0.00)
    active = models.BooleanField(default=False)
    delay = models.IntegerField()