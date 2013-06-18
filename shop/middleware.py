from shop.cart import Cart


class CartMiddleware(object):
    def process_request(self, req):
        c = Cart(req)
        req.cart = c