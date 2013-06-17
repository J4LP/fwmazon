from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from manager.forms import FitForm

from shop.models import DoctrineFit
from manager.utils import Fit

def create(req):
    if req.method == 'POST':
        form = FitForm(req.POST)
        if form.is_valid():
            doctrine = DoctrineFit()
            fit = Fit()
            try:
                fit.import_eft(form.cleaned_data['fit'])
            except:
                messages.error(req, 'Parsing error, make sure the fit is in EFT format')
                return render_to_response('home/create.html', context_instance=RequestContext(req))
            doctrine.ship = fit.ship
            doctrine.fit = fit.to_json()
            doctrine.status = 2 # Calculating price
            doctrine.creator = req.user
            doctrine.save()
            messages.success(req, 'The fit "%s" has been added !' % doctrine.name)
            return redirect(reverse_lazy('shop'))

    else:
        form = FitForm()
    return render_to_response('home/create.html', {'form': form}, context_instance=RequestContext(req))