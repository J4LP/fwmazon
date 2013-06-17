from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


def shop(req):
    return render_to_response('home/shop.html', context_instance=RequestContext(req))
