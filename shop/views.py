from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from shop.models import DoctrineFit
from eve.models import InvType
from django.http import HttpResponse
from cart import CartForm
import json

def shop(req):
    fits = DoctrineFit.objects.all()
    return render_to_response('shop/shop.html', {'fits': fits}, context_instance=RequestContext(req))

def shop_details(req, fit_id):
    fit = DoctrineFit.objects.get(pk=fit_id)
    fit.fit = json.loads(fit.fit)
    modules = [InvType.objects.get(pk=x['id']) for x in fit.fit['modules']]
    drones = [{'item':InvType.objects.get(pk=x['id']), 'amount': x['amount']} for x in fit.fit['drones']]
    return render_to_response('shop/fit_details.html', {'fit': fit, 'modules': modules, 'drones': drones}, context_instance=RequestContext(req))


def cart_view(req):
    cart = req.cart
    print(cart.length)
    cart.populate()
    return render_to_response('shop/cart.html', {'cart': cart}, context_instance=RequestContext(req))


def cart_add(req):
    if req.method == 'POST':
        form = CartForm(req.POST)
        if form.is_valid():
            req.cart.add(req, form.cleaned_data['item_type'], form.cleaned_data['item_id'], form.cleaned_data['amount'])
        return HttpResponse(req.cart.to_json(), mimetype='application/json')


def cart_update(req):
    if req.method == 'POST':        
        form = CartForm(req.POST)
        if form.is_valid():
            req.cart.update(req, form.cleaned_data['item_type'], form.cleaned_data['item_id'], form.cleaned_data['amount'])
        return HttpResponse(req.cart.to_json(), mimetype='application/json')


def cart_delete(req):
    if req.method == 'POST':        
        form = CartForm(req.POST)
        if form.is_valid():
            req.cart.delete(req, form.cleaned_data['item_type'], form.cleaned_data['item_id'])
        return HttpResponse(req.cart.to_json(), mimetype='application/json')