import json
from django.utils import timezone
from shop.models import DoctrineFit
from django import forms

class CartForm(forms.Form):
    item_id = forms.IntegerField(required=True)
    item_type = forms.CharField(required=True)
    amount = forms.IntegerField(required=False)

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

class Cart():

    def __init__(self, request=None):
        self.total = 0.0
        self.last_updated = timezone.now()
        self.items = {'modules': [], 'ships': []}
        self.length = len(self.items['modules']) + len(self.items['ships'])
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
            self.items = cart['items']
            self.length = cart['length']

    def save(self, req):
        self.last_updated = timezone.now()
        self.length = len(self.items['modules']) + len(self.items['ships'])
        print(len(self.items['modules']) + len(self.items['ships']))
        print(len(self.items['modules']))
        print(len(self.items['ships']))
        print(self.length)
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
        for item in self.items[item_type + 's']:
            if item['id'] == item_id:
                item['amount'] = int(item['amount']) + int(amount)
                break
        else:
            self.items[item_type + 's'].append({'id': item_id, 'amount': int(amount)})
        self.save(req)

    def update(self, req, item_type, item_id, amount):
        for idx, item in enumerate(self.items[item_type + 's']):
            if item['id'] == item_id:
                if int(amount) == 0:
                    del(self.items[item_type + 's'][idx])
                else:
                    item['amount'] = int(amount)
                break
        self.save(req)

    def delete(self, req, item_type, item_id):
        for idx, item in enumerate(self.items[item_type + 's']):
            if item['id'] == item_id:
                del(self.items[item_type + 's'][idx])
                break
        self.save(req)

    def populate(self):
        self.doctrines = []
        self.doctrines_price = 0.0
        for item in self.items['ships']:
            fit = DoctrineFit.objects.get(pk=item['id'])
            fit.amount = item['amount']
            self.doctrines_price += int(fit.amount * fit.price)
            self.doctrines.append(fit)
        for item in self.items['modules']:
            # TODO
            pass


