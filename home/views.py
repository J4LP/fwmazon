from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


def home(req):
    return render_to_response('home/index.html', context_instance=RequestContext(req))

