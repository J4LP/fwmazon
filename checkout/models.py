from django.db import models
from django.contrib.auth.models import User
from eve.models import InvType
from shop.models import DoctrineFit
from decimal import Decimal as d

FITTING_PRICE = d(10000.00)
WAITING = 0
PROCESSING = 1
SHIPPED = 2
CONTRACTED = 3
CANCELED = 99
ORDER_STATUS_CHOICES = (
    (WAITING, 'WAITING'),
    (PROCESSING, 'PROCESSING'),
    (SHIPPED, 'SHIPPED'),
    (CONTRACTED, 'CONTRACTED'),
    (CANCELED, 'CANCELED'),
)

class ShippingDestination(models.Model):
    name = models.CharField(max_length=200)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=0.00)
    active = models.BooleanField(default=False)
    delay = models.IntegerField()

class Order(models.Model):
    """
    Order model
    """
    buyer = models.ForeignKey(User, related_name='orders')
    total_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=0.00)
    elements_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=0.00)
    volume = models.FloatField()
    shipping_fee = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=0.00)
    shipping_destination = models.ForeignKey(ShippingDestination)
    to_be_fitted = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    order_status = models.IntegerField(default=WAITING, choices=ORDER_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def _get_tax(self):
        return (self.elements_price + self.shipping_fee + (FITTING_PRICE if self.to_be_fitted else d(0.0))) * d(0.01)

    def new_order(self, cart, shipping_destination, fitting, user):
        if not hasattr(cart, 'doctrines'):
            cart.populate()
        self.shipping_destination = shipping_destination
        if fitting == 'fitting':
            self.to_be_fitted = True
        self.buyer = user
        elements = []
        for doctrine in cart.doctrines:
            elements.append(OrderElement(element_type='doctrine', doctrine_fit=doctrine))
            self.elements_price += doctrine.price
            #self.volume += doctrine.volume
        """
        for module in cart.modules:
            elements.append(OrderElement(element_type='module', item=module))
        """
        self.save()
        for e in elements:
            e.order = self
            e.save()
        return self
        
    tax = property(_get_tax)


class OrderElement(models.Model):
    """
    An element in an Order
    """
    order = models.ForeignKey(Order, related_name="elements")
    element_type = models.CharField(max_length=20)
    doctrine_fit = models.ForeignKey(DoctrineFit, null=True, blank=True)
    item = models.ForeignKey(InvType, null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=0.00)

    def _get_element(self):
        if self.element_type == 'doctrine':
            return self.doctrine_fit
        else:
            return self.invtype

    element = property(_get_element)