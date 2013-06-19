import json
from django.utils import timezone
from shop.models import DoctrineFit
from django import forms
from collections import Counter

class CartForm(forms.Form):
    item_id = forms.IntegerField(required=True)
    item_type = forms.CharField(required=True)
    amount = forms.IntegerField(required=False)

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

class Cart(object):

    def __init__(self, request=None):
        self.total = 0.0
        self.last_updated = timezone.now()
        self.items = {'module': Counter(), 'ship': Counter()}
        self.length = len(self.items['module']) + len(self.items['ship'])
        if request:
            self.load(request)

    def load(self, req):
        try:
            cart = json.loads(req.session['cart'])
        except:
            pass
        else:
            self.total = cart['total']
            self.last_updated = cart['last_updated']
            self.items = {'module': Counter(cart['items']['module']), 'ship': Counter(cart['items']['ship'])}
            self.length = cart['length']

    def save(self, req):
        self.last_updated = timezone.now()
        self.length = len(self.items['module']) + len(self.items['ship'])
        cart = self.to_json()
        req.session['cart'] = cart

    def to_json(self):
        return json.dumps({
            'total': self.total,
            'length': self.length,
            'last_updated': self.last_updated, 
            'items': self.items,
        }, default=date_handler)

    def add(self, req, item_type, item_id, amount):
        self.items[item_type][item_id] += amount
        self.save(req)

    def update(self, req, item_type, item_id, amount):
        if int(amount) == 0:
            del(self.items[item_type][item_id])
        else:
            self.items[item_type][item_id] = amount
        self.save(req)

    def delete(self, req, item_type, item_id):
        del(self.items[item_type][item_id])
        self.save(req)

    def populate(self):
        self.doctrines = []
        self.doctrines_price = 0.0
        for item_id, amount in self.items['ship'].items():
            print(item_id, amount)
            fit = DoctrineFit.objects.get(pk=item_id)
            fit.amount = amount
            self.doctrines_price += int(fit.amount * fit.price)
            self.doctrines.append(fit)
        for item in self.items['module']:
            # TODO
            pass


