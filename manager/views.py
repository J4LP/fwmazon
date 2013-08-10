from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext
from django.utils import formats
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django_datatables_view.base_datatable_view import BaseDatatableView
from account.models import User
from checkout.models import Order, WAITING, PROCESSING, FINISHED, MONEY_RECEIVED
from eve.models import CorpWallet
from manager.forms import FitForm
from manager.utils import Fit
from manager.tasks import update_fit
from shop.models import DoctrineFit
import logging
l = logging.getLogger('fwmazon')


class ManagerFitCreation(FormView):
    template_name = 'manager/create.html'
    form_class = FitForm
    success_url = reverse_lazy('manager-list-fits')

    def form_valid(self, form):
        fit = Fit()
        try:
            fit.import_eft(form.cleaned_data['fit'])
        except:
            l.error('Could not create fit, parsing error', exc_info=1, extra={'user_id': self.request.user.id, 'request': self.request})
            messages.error(self.request, 'Parsing error, make sure the fit is in EFT format')
            return redirect(reverse_lazy('manager-create-fit'))
        doctrine = DoctrineFit(
            name=fit.fit_name,
            description=form.cleaned_data['description'],
            ship=fit.ship,
            fit=fit.to_json(),
            status=2,
            creator=self.request.user,
        )
        doctrine.save()
        doctrine.create_elements()
        update_fit(doctrine.id)
        l.info('Fit #%s created by user#%s' % (doctrine.id, self.request.user.id), extra={'user_id': self.request.user.id, 'request': self.request})
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
        waiting_queue = Order.objects.filter(payment__status=MONEY_RECEIVED).filter(order_status=WAITING).order_by('priority_flag').order_by('-payment__updated_at')
        processing_queue = Order.objects.filter(payment__status=MONEY_RECEIVED).exclude(order_status=WAITING).exclude(order_status=FINISHED).order_by('updated_at').order_by('-order_status')
        delivered_queue = Order.objects.filter(payment__status=MONEY_RECEIVED).filter(order_status=FINISHED).order_by('-updated_at')
        context['waiting_queue'] = waiting_queue
        context['processing_queue'] = processing_queue
        context['delivered_queue'] = delivered_queue
        return context


class ManagerOrderAccept(View):
    def post(self, request, order_id, **kwargs):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            l.error('Order.DoesNotExist Order#%s' % order_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            messages.error(request, 'Could not find order.')
            return redirect(reverse_lazy('manager-queue'))
        if order.contractor == request.user:
            l.error('Order.AlreadyTakingCare Order#%s' % order_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            messages.error(request, 'You are already taking care of this order, nerd.')
            return reverse_lazy('manager-order', kwargs={'order_id': order.id})
        if order.contractor is not None and order.contractor != request.user:
            l.error('Order.SomeoneElseHas Order#%s' % order_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            messages.error(request, 'This order is already being taken care of by someone else.')
            return redirect(reverse_lazy('manager-queue'))
        if order.order_status != WAITING:
            l.error('Order.UndefinedError Order#%s' % order_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            messages.error(request, 'An undefined error occured.')
            return redirect(reverse_lazy('manager-queue'))
        if len(request.user.orders_contracted.filter(~Q(order_status=4))) > 2:
            l.error('Order.MaximumContractedOrders Order#%s' % order_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            messages.error(request, 'You already have contracted the maximum of orders allowed.')
            return redirect(reverse_lazy('manager-queue'))
        order.contractor = request.user
        order.order_status = PROCESSING
        order.save()
        messages.success(request, 'You are now taking care of this order. Here\'s the details:')
        return redirect(reverse_lazy('manager-order', kwargs={'order_id': order.id}))


class ManagerOrder(View):
    template_name = 'manager/order.html'

    def get(self, request, order_id, **kwargs):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            l.error('Order.DoesNotExist Order#%s' % order_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            messages.error(request, 'Could not find order.')
            return redirect(reverse_lazy('manager-queue'))
        if not request.user.is_contractor:
            if order.contractor != request.user:
                l.error('Order.NotContracted Order#%s' % order_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
                messages.error(request, 'You are not contracted to this order, you\'re bad.')
                return redirect(reverse_lazy('manager-queue'))
        return render_to_response(self.template_name, {'order': order}, context_instance=RequestContext(request))


class ManagerOrderUpdate(View):
    def post(self, request, order_id, **kwargs):
        # Status validation
        if not 'status' in request.POST:
            l.error('FormValidationError Order#%s' % order_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            messages.error(request, 'Form validation error')
            return redirect(reverse_lazy('manager-queue'))
        status = int(request.POST['status'][0])
        if not status in [2, 3]:
            l.error('FormValidationError Order#%s' % order_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            messages.error(request, 'Form validation error')
            return redirect(reverse_lazy('manager-queue'))
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            l.error('Order.DoesNotExist Order#%s' % order_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            messages.error(request, 'Could not find order.')
            return redirect(reverse_lazy('manager-queue'))
        if order.contractor is None or order.contractor != request.user:
            l.error('Order.SomeoneElseHas Order#%s' % order_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            messages.error(request, 'This order is already being taken care of by someone else.')
            return redirect(reverse_lazy('manager-queue'))
        if order.order_status == WAITING:
            l.error('Order.NotAcceptedYet Order#%s' % order_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            messages.error(request, 'This order hasn\'t been accepted yet.')
            return redirect(reverse_lazy('manager-queue'))

        order.order_status = request.POST['status']
        order.save()
        l.info('Order.Updated Order#%s -> %s' % (order_id, request.POST['status']), exc_info=1, extra={'user_id': request.user.id, 'request': request})
        messages.success(request, 'Order successfully updated')
        return redirect(reverse_lazy('manager-order', kwargs={'order_id': order.id}))


class ManagerWalletList(TemplateView):
    template_name = 'manager/wallet_list.html'

    def get_context_data(self, **kwargs):
        context = super(ManagerWalletList, self).get_context_data(**kwargs)
        context['wallets'] = CorpWallet.objects.all()
        return context


class ManagerWalletDetails(View):
    template_name = 'manager/wallet_details.html'

    def get(self, request, wallet_id):
        try:
            wallet = CorpWallet.objects.select_related().get(pk=wallet_id)
        except CorpWallet.DoesNotExist:
            l.error('CorpWallet.DoesNotExist Wallet#%s' % wallet_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            messages.error(request, 'Could not find wallet')
            return redirect(reverse_lazy('manager-wallets'))
        return render_to_response(self.template_name, {'wallet': wallet}, context_instance=RequestContext(request))


class ManagerOrders(TemplateView):
    template_name = 'manager/orders.html'

    def get_context_data(self, **kwargs):
        context = super(ManagerOrders, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.all()[:20]
        return context


class ManagerOrdersDataTable(BaseDatatableView):
    model = Order
    columns = ['id', 'buyer', 'order_status', 'shipping_destination', 'total_price', 'created_at', 'actions']
    order_columns = ['id', 'buyer', 'order_status', 'shipping_destination', 'total_price', 'created_at', '']
    max_display_length = 30

    def render_column(self, row, column):
        if column == 'order_status':
            if row.order_status == 0:
                return '<span class="text-muted">%s</span>' % row.get_order_status_display()
            elif row.order_status == 1 or row.order_status == 2 or row.order_status == 3:
                return '<span class="text-warning">%s</span>' % row.get_order_status_display()
            elif row.order_status == 4:
                return '<span class="text-success">%s</span>' % row.get_order_status_display()
            else:
                return '<span class="text-danger">%s</span>' % row.get_order_status_display()
        if column == 'buyer':
            return row.buyer.character.name
        if column == 'total_price':
            return '%s ISK' % intcomma(row.total_price)
        if column == 'shipping_destination':
            return row.shipping_destination.short_name
        if column == 'created_at':
            return formats.date_format(row.created_at, "SHORT_DATETIME_FORMAT")
        if column == 'actions':
            return '<a href="/manager/order/%s" class="btn btn-info btn-small">Info</a>' % row.id
        return super(ManagerOrdersDataTable, self).render_column(row, column)


class ManagerContractors(TemplateView):
    template_name = 'manager/contractors.html'

    def get_context_data(self, **kwargs):
        context = super(ManagerContractors, self).get_context_data(**kwargs)
        context['contractors'] = User.objects.filter(Q(is_contractor=True) | Q(is_manager=True))
        return context


class ManagerContractorsDataTable(BaseDatatableView):
    model = User
    columns = ['username', 'character', 'email', 'orders_contracted', 'last_login', 'actions']
    order_columns = ['username', 'character', 'email', 'orders_contracted', 'last_login', '']
    max_display_length = 30

    def render_column(self, row, column):
        if column == 'character':
            return row.character.name
        if column == 'orders_contracted':
            return len(row.orders_contracted.all())
        if column == 'last_login':
            return formats.date_format(row.last_login, "SHORT_DATETIME_FORMAT")
        if column == 'actions':
            return '<a href="/manager/contractor/%s" class="btn btn-info btn-small">Profile</a>' % row.id
        return super(ManagerContractorsDataTable, self).render_column(row, column)

    def filter_queryset(self, qs):
        return qs.filter(Q(is_contractor=True)|Q(is_manager=True))


class ManagerContractor(TemplateView):
    template_name = 'manager/contractor.html'
    
    def get(self, request, user_id):
        try:
            user = User.objects.select_related().get(pk=user_id)
        except User.DoesNotExist:
            l.error('User.DoesNotExist', exc_info=1, extra={'user_id': user_id, 'request': request})
            messages.error(request, 'Could not find contractor')
            return redirect(reverse_lazy('manager-contractors'))
        orders_pending = user.orders_contracted.filter(order_status=PROCESSING)
        return render_to_response(self.template_name, {'user': user, 'orders_pending': orders_pending}, context_instance=RequestContext(request))