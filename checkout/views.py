from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from checkout.models import ShippingDestination
from django.views.generic import View
from checkout.models import Order
from django.contrib import messages


class CheckoutView(View):
    template_name = 'checkout/checkout.html'

    def get(self, req):
        # TODO: check if cart is empty
        destinations = ShippingDestination.objects.filter(active=True)
        cart = req.cart
        cart.populate()
        return render_to_response(self.template_name, {'destinations': destinations, 'cart': cart}, context_instance=RequestContext(req))

    def post(self, req):
        shipping_destination, fitting = req.POST['shipping'], req.POST['fitting'] if 'fitting' in req.POST else None
        order = Order()
        try:
            shipping_destination = ShippingDestination.objects.get(pk=shipping_destination)
            if not shipping_destination.active:
                messages.error(req, 'Something happen while creating your order, please try again.')
                return render_to_response(self.template_name, context_instance=RequestContext(req))
        except ShippingDestination.DoesNotExist:
            messages.error(req, 'Something happen while creating your order, please try again.')
            return render_to_response(self.template_name, context_instance=RequestContext(req))
        try:
            order.new_order(req.cart, shipping_destination, fitting, req.user)
        except Exception:
            messages.error(req, 'Something happen while creating your order, please try again.')
            return render_to_response(self.template_name, context_instance=RequestContext(req))
        else:
            # TODO: clear the cart
            messages.success(req, 'Your order has been successfully created, please proceed with the payment.')
            return redirect('/checkout/pay/' + order.id)


class PayView(View):
    template_name = 'checkout/pay.html'

    def get(self, req, order_id):
        order = Order.objects.get(pk=order_id)
        if order.buyer != req.user:
            messages.error(req, 'Security error, are you logged in ?')
            return redirect('/')
        if order.paid:
            messages.info(req, 'This order has already been paid')
            return redirect('/account')
        return render_to_response(self.template_name, {'order': order}, context_instance=RequestContext(req))