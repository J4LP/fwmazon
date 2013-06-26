from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from manager.forms import FitForm
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from shop.models import DoctrineFit
from manager.utils import Fit
from django.shortcuts import redirect


class ManagerFitCreation(FormView):
    template_name = 'manager/create.html'
    form_class = FitForm
    success_url = reverse_lazy('manager-list-fits')

    def form_valid(self, form):
        fit = Fit()
        try:
            fit.import_eft(form.cleaned_data['fit'])
        except:
            messages.error(self.request, 'Parsing error, make sure the fit is in EFT format')
            return redirect(reverse_lazy('manager-create-fit'))

        doctrine = DoctrineFit(
            name=fit.fit_name,
            description=form.cleaned_data['description'],
            ship=fit.ship,
            fit=fit.to_json(),
            status=2,
            creator=self.request.user,
        ).save()
        messages.success(self.request, 'The fit "%s" has been added !' % doctrine.name)
        return super(ManagerFitCreation, self).form_valid(form)

class ManagerFitList(TemplateView):
    template_name = 'manager/list_fits.html'

    def get_context_data(self, **kwargs):
        context = super(ManagerFitList, self).get_context_data(**kwargs)
        context['fits'] = DoctrineFit.objects.all()
        return context


class ManagerQueue(TemplateView):
    template_name = 'manager/queue.html'
    