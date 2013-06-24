from django.views.generic import TemplateView


class AccountHomeView(TemplateView):
    template_name = "account/account.html"

    def get_context_data(self, **kwargs):
        context = super(AccountHomeView, self).get_context_data(**kwargs)
        return context
