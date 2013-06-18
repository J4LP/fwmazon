from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from shop.models import DoctrineFit
from eve.models import InvType
import json

def shop(req):
    print(req.META.get('REMOTE_ADDR'))
    print(req.cart)
    fits = DoctrineFit.objects.all()
    return render_to_response('shop/shop.html', {'fits': fits}, context_instance=RequestContext(req))

def shop_details(req, fit_id):
    fit = DoctrineFit.objects.get(pk=fit_id)
    fit.fit = json.loads(fit.fit)
    modules = [InvType.objects.get(pk=x['id']) for x in fit.fit['modules']]
    drones = [{'item':InvType.objects.get(pk=x['id']), 'amount': x['amount']} for x in fit.fit['drones']]
    return render_to_response('shop/fit_details.html', {'fit': fit, 'modules': modules, 'drones': drones}, context_instance=RequestContext(req))