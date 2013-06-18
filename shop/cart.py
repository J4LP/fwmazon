import json
from django.utils import timezone
from shop.models import DoctrineFit

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

class Cart():

    def __init__(self, request=None):
        self.total = 0.0
        self.last_updated = timezone.now()
        self.items = []
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

    def save(self, req):
        self.last_updated = timezone.now()
        cart = self.to_json()
        req.session['cart'] = cart

    def to_json(self):
        return json.dumps({'total': self.total, 'last_updated': self.last_updated, 'items': self.items}, default=date_handler)

    def add_doctrine(self, req, doctrine_id, amount):
        for item in self.items:
            if item['type'] == 'doctrine' and item['doctrine_id'] == doctrine_id:
                item['amount'] = int(item['amount'])
                item['amount'] += int(amount)
                break
        else:
            self.items.append({'type': 'doctrine', 'doctrine_id': doctrine_id, 'amount': int(amount)})
        self.save(req)

    def populate(self):
        self.doctrines = []
        self.doctrines_price = 0.0
        for item in self.items:
            if item['type'] == 'doctrine':
                fit = DoctrineFit.objects.get(pk=item['doctrine_id'])
                fit.amount = item['amount']
                self.doctrines_price += int(fit.amount * fit.price)
                self.doctrines.append(fit)


