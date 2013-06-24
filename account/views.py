from fwmazon.views import FwmazonTemplateView
from django.shortcuts import redirect
from checkout.models import Order
from django.contrib import messages


class AccountHomeView(FwmazonTemplateView):
    template_name = "account/account.html"

    def get_request_context_data(self, request, **kwargs):
        context = super(AccountHomeView, self).get_context_data(**kwargs)
        context['orders'] = request.user.orders.all()
        return context


class AccountOrdersView(FwmazonTemplateView):
    template_name = "account/orders.html"

    def get_request_context_data(self, request, **kwargs):
        context = super(AccountOrdersView, self).get_context_data(**kwargs)
        context['orders'] = request.user.orders.all()
        return context


class AccountOrderDetailView(FwmazonTemplateView):
    template_name = "account/order_details.html"

    def get_request_context_data(self, request, **kwargs):
        context = super(AccountOrderDetailView, self).get_context_data(**kwargs)
        try:
            order = Order.objects.get(pk=kwargs['order_id'])
        except Order.DoesNotExist:
            messages.error(request, 'Could not find the order.')
            return redirect('/')
        if order.buyer != request.user:
            messages.error(request, 'Security error, are you logged in ?')
            return redirect('/')
        context['order'] = order
        return context
