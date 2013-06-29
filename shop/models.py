from django.db import models
from django.contrib.auth.models import User
from eve.models import InvType
from collections import Counter
import json


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

    def create_elements(self):
        fit = json.loads(self.fit)
        DoctrineElement(doctrine=self, element_type='ship', item=InvType.objects.get(pk=fit['ship']['ship_id']), amount=1).save()
        modules = Counter()
        drones = Counter()
        for module in fit['modules']:
            modules[str(module['id'])] += 1
        for drone in fit['drones']:
            drones[str(drone['id'])] += drone['amount']
        for item_id, amount in modules.items():
            DoctrineElement(doctrine=self, element_type='module', item=InvType.objects.get(pk=item_id), amount=amount).save()
        for item_id, amount in drones.items():
            DoctrineElement(doctrine=self, element_type='drone', item=InvType.objects.get(pk=item_id), amount=amount).save()


class DoctrineElement(models.Model):
    doctrine = models.ForeignKey(DoctrineFit, related_name="elements")
    element_type = models.CharField(max_length=20)
    item = models.ForeignKey(InvType, null=True, blank=True)
    amount = models.IntegerField(default=1)
