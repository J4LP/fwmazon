from fwmazon.views import FwmazonTemplateView


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
