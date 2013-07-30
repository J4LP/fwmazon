import logging
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import View
from django.views.generic.base import TemplateView
from checkout.models import MONEY_RECEIVED, MONEY_SENT, Order, ShippingDestination

l = logging.getLogger('fwmazon')


class CheckoutView(View):
    template_name = 'checkout/checkout.html'

    def get(self, request):
        if request.cart.length == 0:
            messages.info(request, 'Your cart is empty, you should put some ships in it !')
            return redirect(reverse_lazy('shop'))
        destinations = ShippingDestination.objects.filter(active=True)
        if len(destinations) == 0:
            messages.error(request, 'There is no shipping destination available, we are fixing it !')
            l.error('ShippingDestination.NoneActive', extra={'user_id': request.user.id, 'request': request})
            return redirect(reverse_lazy('cart'))
        request.cart.populate()
        return render_to_response(self.template_name, {'destinations': destinations, 'cart': request.cart}, context_instance=RequestContext(request))

    def post(self, request):
        # shipping_destination, fitting = request.POST['shipping'], request.POST['fitting'] if 'fitting' in request.POST else None
        shipping_destination, fitting = request.POST['shipping'], None
        order = Order()
        try:
            shipping_destination = ShippingDestination.objects.get(pk=shipping_destination)
            if not shipping_destination.active:
                messages.error(request, 'Something happen while creating your order, please try again. #1')
                return redirect(reverse_lazy('checkout'))
        except ShippingDestination.DoesNotExist:
            messages.error(request, 'Something happen while creating your order, please try again. #2')
            return redirect(reverse_lazy('checkout'))
        try:
            order.new_order(request.cart, shipping_destination, fitting, request.user)
        except Exception:
            messages.error(request, 'Something happen while creating your order, please try again. #3')
            return redirect(reverse_lazy('checkout'))
        else:
            request.cart.clear(request)
            l.info('Order.OrderCreated #%s' % order.id, extra={'user_id': request.user.id, 'request': request})
            messages.success(request, 'Your order has been successfully created, please proceed with the payment.')
            return redirect(reverse_lazy('checkout-pay', kwargs={'order_id': order.id}))


class PayView(View):
    template_name = 'checkout/pay.html'

    def get(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            messages.error(request, 'This order does not exist')
            l.error('Order.DoesNotExist #%s' % order_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            return redirect(reverse_lazy('account-order'))
        if order.buyer != request.user:
            messages.error(request, 'Security error, are you logged in ?')
            l.error('Order.SecurityError #%s' % order_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            return redirect('/')
        if order.is_paid:
            messages.info(request, 'This order has already been paid')
            return redirect(reverse_lazy('account-order'))
        return render_to_response(self.template_name, {'order': order}, context_instance=RequestContext(request))

    def post(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            messages.error(request, 'This order does not exist')
            l.error('Order.DoesNotExist #%s' % order_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            return redirect(reverse_lazy('account-order'))
        if order.buyer != request.user:
            l.error('Order.SecurityError #%s' % order_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            messages.error(request, 'Security error, are you logged in ?')
            return redirect('/')
        if order.is_paid or order.payment.status == MONEY_RECEIVED:
            messages.info(request, 'This order has already been paid')
            return redirect(reverse_lazy('account-order'))
        order.payment.status = MONEY_SENT
        order.payment.save()
        messages.info(request, 'We are now processing your order, thanks you for using Fwmazon !')
        return redirect(reverse_lazy('checkout-thanksyou'))


class ThanksYouView(TemplateView):
    template_name = 'checkout/thanks.html'