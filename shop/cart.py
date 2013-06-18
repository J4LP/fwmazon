import json
from django.utils import timezone

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
        cart = json.dumps({'total': self.total, 'last_updated': self.last_updated, 'items': self.items})
        req.session['cart'] = cart

