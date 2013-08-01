import logging
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import TemplateView
from django.views.generic.base import View
from checkout.models import Order

l = logging.getLogger('fwmazon')


class AccountHomeView(TemplateView):
    template_name = "account/account.html"

    def get_context_data(self, **kwargs):
        context = super(AccountHomeView, self).get_context_data(**kwargs)
        context['orders'] = self.request.user.orders.all().order_by("-id")[:20]
        return context


class AccountOrdersView(TemplateView):
    template_name = "account/orders.html"

    def get_context_data(self, **kwargs):
        context = super(AccountOrdersView, self).get_context_data(**kwargs)
        context['orders'] = self.request.user.orders.all()
        return context


class AccountOrderDetailView(View):
    template_name = "account/order_details.html"

    def get(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            messages.error(request, 'Could not find the order.')
            return redirect('/')
        if order.buyer != request.user:
            l.error('PermissionDenied', exc_info=1, extra={
                    'user_id': request.user.id, 'request': request})
            raise PermissionDenied
        return render_to_response(self.template_name, {'order': order}, context_instance=RequestContext(request))


class AccountOrderCancelView(View):

    def post(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            messages.error(request, 'Could not find the order.')
            return redirect('/')
        if order.buyer != request.user:
            l.error('PermissionDenied', exc_info=1, extra={
                    'user_id': request.user.id, 'request': request})
            raise PermissionDenied
        order.order_status = 99
        order.save()
        l.info('Order cancelled by user action', extra={
               'user_id': request.user.id, 'request': request})
        return redirect(reverse_lazy('account-orders'))
