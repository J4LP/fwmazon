from django.db import models
from django.contrib.auth.models import User
from eve.models import InvType

class DoctrineFit(models.Model):
    """
    Model for the doctrine fit in the shop
    """
    ship = models.ForeignKey(InvType)
    name = models.CharField(max_length=100)
    description = models.TextField()
    fit = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=0.00)
    """
    0 : deactivated
    1 : activated
    2 : calculating price
    """
    status = models.IntegerField(default=0)
    bought = models.IntegerField(default=0)
    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

