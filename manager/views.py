from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from manager.forms import FitForm
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from shop.models import DoctrineFit
from manager.utils import Fit
from django.shortcuts import redirect
from checkout.models import Order, WAITING, FINISHED
from django.views.generic.base import View


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

    def get_context_data(self, **kwargs):
        context = super(ManagerQueue, self).get_context_data(**kwargs)
        waiting_queue = Order.objects.filter(paid=True).filter(order_status=WAITING).order_by('priority_flag').order_by('-paid_date')
        processing_queue = Order.objects.filter(paid=True).exclude(order_status=WAITING).exclude(order_status=FINISHED).order_by('-order_status').order_by('-updated_at')
        delivered_queue = Order.objects.filter(paid=True).filter(order_status=FINISHED).order_by('-updated_at')
        context['waiting_queue'] = waiting_queue
        context['processing_queue'] = processing_queue
        context['delivered_queue'] = delivered_queue
        return context


class ManagerAcceptOrder(View):
    def post(self, request, order_id, **kwargs):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            messages.error(request, 'Could not find order.')
            return redirect(reverse_lazy('manager-queue'))
        if order.status != 0 or order.contractor is not None:
            messages.error(request, 'This order is already being taken care of.')
            return redirect(reverse_lazy('manager-queue'))
        # TODO : Add check for number of orders https://github.com/Fweddit/fwmazon/issues/1
        # TODO : Check if the user can contract the orders
        order.worker = request.user
        order.save()
        #messages.success(request, 'You are now taking care of this order. Here\'s the details :')
        #return redirect(reverse_lazy('manager-order-details', order.id))
        return redirect(reverse_lazy('manager-queue'))