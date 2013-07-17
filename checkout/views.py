from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from checkout.models import ShippingDestination
from django.views.generic import View
from checkout.models import Order
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from checkout.models import MONEY_RECEIVED, MONEY_SENT


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
                messages.error(req, 'Something happen while creating your order, please try again. #1')
                return redirect(reverse_lazy('checkout'))
        except ShippingDestination.DoesNotExist:
            messages.error(req, 'Something happen while creating your order, please try again. #2')
            return redirect(reverse_lazy('checkout'))
        try:
            order.new_order(req.cart, shipping_destination, fitting, req.user)
        except Exception:
            messages.error(req, 'Something happen while creating your order, please try again. #3')
            return redirect(reverse_lazy('checkout'))
        else:
            # TODO: clear the cart
            messages.success(req, 'Your order has been successfully created, please proceed with the payment.')
            return redirect(reverse_lazy('checkout-pay', order_id=order.id))


class PayView(View):
    template_name = 'checkout/pay.html'

    def get(self, req, order_id):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            messages.error(req, 'This order does not exist')
            return redirect(reverse_lazy('account-order'))
        if order.buyer != req.user:
            messages.error(req, 'Security error, are you logged in ?')
            return redirect('/')
        if order.is_paid:
            messages.info(req, 'This order has already been paid')
            return redirect(reverse_lazy('account-order'))
        return render_to_response(self.template_name, {'order': order}, context_instance=RequestContext(req))

    def post(self, req, order_id):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            messages.error(req, 'This order does not exist')
            return redirect(reverse_lazy('account-order'))
        if order.buyer != req.user:
            messages.error(req, 'Security error, are you logged in ?')
            return redirect('/')
        if order.is_paid or order.payment.status == MONEY_RECEIVED:
            messages.info(req, 'This order has already been paid')
            return redirect(reverse_lazy('account-order'))
        order.payment.status = MONEY_SENT
        order.payment.save()
        messages.info(req, 'We are now processing your order, thanks for using Fwmazon')
        # TODO : Make a thank you page, test if payment status is already sent
        return redirect(reverse_lazy('account-orders'))
