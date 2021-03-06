from django.db import models
from account.models import User
from eve.models import InvType, CorpWalletJournalEntry
from shop.models import DoctrineFit
from decimal import Decimal as d
import random
import string

FITTING_PRICE = d(10000.00)
WAITING = 0
PROCESSING = 1
SHIPPED = 2
CONTRACTED = 3
FINISHED = 4
CANCELLED = 99
ORDER_STATUS_CHOICES = (
    (WAITING, 'Waiting'),
    (PROCESSING, 'Processing'),
    (SHIPPED, 'Shipped'),
    (CONTRACTED, 'Contracted'),
    (FINISHED, 'Finished'),
    (CANCELLED, 'Cancelled'),
)
MONEY_SENT = 1
MONEY_RECEIVED = 2
PAYMENT_STATUS_CHOICES = (
    (WAITING, 'Waiting for payment'),
    (MONEY_SENT, 'Money sent'),
    (MONEY_RECEIVED, 'Money received')
)


class QuerySetManager(models.Manager):
    def get_query_set(self):
        return self.model.QuerySet(self.model)

    def __getattr__(self, attr, *args):
        return getattr(self.get_query_set(), attr, *args)


class ShippingDestination(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=64)
    system = models.CharField(max_length=64)
    shipping_cost = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=0.00)
    active = models.BooleanField(default=False)
    delay = models.IntegerField()


class Order(models.Model):
    """
    Order model
    """
    buyer = models.ForeignKey(User, related_name='orders')
    contractor = models.ForeignKey(User, related_name='orders_contracted', null=True)
    payment = models.ForeignKey('Payment', related_name='order')
    total_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=d(0.00))
    elements_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=d(0.00))
    volume = models.FloatField(default=0.0)
    shipping_fee = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=d(0.00))
    shipping_destination = models.ForeignKey(ShippingDestination)
    to_be_fitted = models.BooleanField(default=False)
    priority_flag = models.BooleanField(default=False)
    order_status = models.IntegerField(default=WAITING, choices=ORDER_STATUS_CHOICES)
    contracted_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def _get_tax(self):
        return (self.elements_price + self.shipping_fee + (FITTING_PRICE if self.to_be_fitted else d(0.0))) * d(0.01)

    def _get_is_paid(self):
        return True if self.payment.status == 2 else False

    def new_order(self, cart, shipping_destination, fitting, user):
        if not hasattr(cart, 'doctrines'):
            cart.populate()
        self.shipping_destination = shipping_destination
        if fitting == 'fitting':
            self.to_be_fitted = True
        self.buyer = user
        # Calculating prices
        self.total_price = d(0)
        self.elements_price = d(0)
        self.shipping_fee = d(cart.volume) * self.shipping_destination.shipping_cost
        self.volume = cart.volume
        elements = []
        for doctrine in cart.doctrines:
            elements.append(OrderElement(element_type='doctrine', doctrine_fit=doctrine, amount=doctrine.amount))
            self.elements_price += doctrine.price
            #self.volume += doctrine.volume
        """
        for module in cart.modules:
            elements.append(OrderElement(element_type='module', item=module))
        """
        self.total_price = self.elements_price + self.shipping_fee + (FITTING_PRICE if self.to_be_fitted else d(0.0)) + self.tax
        p = Payment()
        p.generate_key()
        p.save()
        self.payment = p
        self.save()
        for e in elements:
            e.order = self
            e.save()
        return self

    tax = property(_get_tax)
    is_paid = property(_get_is_paid)
    objects = QuerySetManager()

    class QuerySet(models.query.QuerySet):

        def current(self):
            return self.filter(order_status=WAITING)

        def finished(self):
            return self.filter(order_status=FINISHED)

        def cancelled(self):
            return self.filter(order_status=CANCELLED)


class OrderElement(models.Model):
    """
    An element in an Order
    """
    order = models.ForeignKey(Order, related_name="elements")
    element_type = models.CharField(max_length=20)
    doctrine_fit = models.ForeignKey(DoctrineFit, null=True, blank=True)
    item = models.ForeignKey(InvType, null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=0.00)
    amount = models.IntegerField(max_length=5)

    def _get_element(self):
        if self.element_type == 'doctrine':
            return self.doctrine_fit
        else:
            return self.invtype

    element = property(_get_element)

    objects = QuerySetManager()

    class QuerySet(models.query.QuerySet):

        def ship(self):
            return self.filter(element_type="doctrine")

        def item(self):
            return self.filter(element_type="item")


class Payment(models.Model):
    status = models.IntegerField(default=WAITING, choices=ORDER_STATUS_CHOICES)
    key = models.CharField(max_length=35)
    transaction = models.ForeignKey(CorpWalletJournalEntry, null=True, related_name='payment')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def generate_key(self):
        self.key = ''.join(random.choice(string.lowercase + string.uppercase + string.digits) for x in range(35))
