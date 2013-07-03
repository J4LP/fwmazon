from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from manager.forms import FitForm
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from shop.models import DoctrineFit
from manager.utils import Fit
from django.shortcuts import redirect
from checkout.models import Order, WAITING, PROCESSING, FINISHED
from django.views.generic.base import View
from django.shortcuts import render_to_response
from django.template.context import RequestContext


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
        doctrine.create_elements()
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
        processing_queue = Order.objects.filter(paid=True).exclude(order_status=WAITING).exclude(order_status=FINISHED).order_by('updated_at').order_by('-order_status')
        delivered_queue = Order.objects.filter(paid=True).filter(order_status=FINISHED).order_by('-updated_at')
        context['waiting_queue'] = waiting_queue
        context['processing_queue'] = processing_queue
        context['delivered_queue'] = delivered_queue
        return context


class ManagerOrderAccept(View):
    def post(self, request, order_id, **kwargs):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            messages.error(request, 'Could not find order.')
            return redirect(reverse_lazy('manager-queue'))
        if order.contractor == request.user:
            messages.error(request, 'You are already taking care of this order, nerd.')
            return redirect(reverse_lazy('manager-order-details', kwargs={'order_id': order.id}))
        if order.contractor is not None and order.contractor != request.user:
            messages.error(request, 'This order is already being taken care of by someone else.')
            return redirect(reverse_lazy('manager-queue'))
        if order.order_status != WAITING:
            messages.error(request, 'An undefined error occured.')
            return redirect(reverse_lazy('manager-queue'))
        # TODO : Add check for number of orders https://github.com/Fweddit/fwmazon/issues/1
        # TODO : Check if the user can contract the orders
        order.contractor = request.user
        order.order_status = PROCESSING
        order.save()
        messages.success(request, 'You are now taking care of this order. Here\'s the details:')
        return redirect(reverse_lazy('manager-order-details', kwargs={'order_id': order.id}))


class ManagerOrderDetails(View):
    template_name = 'manager/order_details.html'

    def get(self, request, order_id, **kwargs):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            messages.error(request, 'Could not find order.')
            return redirect(reverse_lazy('manager-queue'))
        if order.contractor != request.user:
            messages.error(request, 'You are not contracted to this order, you\'re bad.')
            return redirect(reverse_lazy('manager-queue'))
        return render_to_response(self.template_name, {'order': order}, context_instance=RequestContext(request))


class ManagerOrderUpdate(View):
    def post(self, request, order_id, **kwargs):
        # Status validation
        print(request.POST)
        if not 'status' in request.POST:
            messages.error(request, 'Form validation error')
            return redirect(reverse_lazy('manager-queue'))
        status = int(request.POST['status'][0])
        if not status in [2, 3]:
            messages.error(request, 'Form validation error')
            return redirect(reverse_lazy('manager-queue'))
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            messages.error(request, 'Could not find order.')
            return redirect(reverse_lazy('manager-queue'))
        if order.contractor is None or order.contractor != request.user:
            messages.error(request, 'This order is already being taken care of by someone else.')
            return redirect(reverse_lazy('manager-queue'))
        if order.order_status == WAITING:
            messages.error(request, 'This order hasn\'t been accepted yet.')
            return redirect(reverse_lazy('manager-queue'))

        order.order_status = request.POST['status']
        order.save()
        messages.success(request, 'Order successfully updated')
        return redirect(reverse_lazy('manager-order-details', kwargs={'order_id': order.id}))
