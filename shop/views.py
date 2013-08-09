import json
import logging
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView
from eve.models import InvType
from shop.cart import CartForm
from shop.models import DoctrineFit

l = logging.getLogger('fwmazon')


class ShopView(ListView):
    model = DoctrineFit
    template_name = 'shop/shop.html'

    def get_context_data(self, **kwargs):
        context = super(ShopView, self).get_context_data(**kwargs)
        if 'cart_modified' in self.request.session:
            context['cart_modified'] = True
            del(self.request.session['cart_modified'])
        return context


class DoctrineDetailsView(View):
    template_name = 'shop/fit_details.html'

    def get(self, request, fit_id):
        try:
            fit = DoctrineFit.objects.get(pk=fit_id)
        except DoctrineFit.DoesNotExist:
            l.error('DoctrineFit.DoesNotExist DoctrineFit#%s' % fit_id, exc_info=1, extra={'user_id': request.user.id, 'request': request})
            messages.error(request, 'Could not find this doctrine fit')
            return redirect(reverse_lazy('shop'))
        fit.fit = json.loads(fit.fit)
        modules = [InvType.objects.get(pk=x['id']) for x in fit.fit['modules']]
        drones = [{'item':InvType.objects.get(pk=x['id']), 'amount': x['amount']} for x in fit.fit['drones']]
        return render_to_response(self.template_name, {'fit': fit, 'modules': modules, 'drones': drones}, context_instance=RequestContext(request))


class CartView(TemplateView):
    template_name = 'shop/cart.html'
    
    def get(self, request):
        if self.request.cart.length == 0:
            messages.info(request, 'Your cart is empty, you should put some ships in it !')
            return redirect(reverse_lazy('shop'))
        self.request.cart.populate()
        return render_to_response(self.template_name, {'cart': self.request.cart}, context_instance=RequestContext(request))


class CartAddView(View):
    def post(self, request):
        form = CartForm(request.POST)
        if form.is_valid():
            request.cart.add(request, form.cleaned_data['item_type'], form.cleaned_data['item_id'], form.cleaned_data['amount'])
        request.session['cart_modified'] = True
        return HttpResponse(request.cart.to_json(), mimetype='application/json')


class CartUpdateView(View):
    def post(self, request):
        form = CartForm(request.POST)
        if form.is_valid():
            request.cart.update(request, form.cleaned_data['item_type'], form.cleaned_data['item_id'], form.cleaned_data['amount'])
            request.session['cart_modified'] = True
        return HttpResponse(request.cart.to_json(), mimetype='application/json')


class CartDeleteView(View):
    def post(self, request):
        form = CartForm(request.POST)
        if form.is_valid():
            request.cart.delete(request, form.cleaned_data['item_type'], form.cleaned_data['item_id'])
            request.session['cart_modified'] = True
        return HttpResponse(request.cart.to_json(), mimetype='application/json')
