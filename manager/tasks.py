from celery import task
from eve.models import ItemPrice
from shop.models import DoctrineFit
from django.utils import timezone
import json
from decimal import Decimal
from eve.models import ItemPrice, InvType

# TODO: Add ammo support, and we can do better
@task()
def update_fit(fit_id):
    try:
        doctrine_fit = DoctrineFit.objects.get(pk=fit_id)
    except DoctrineFit.DoesNotExist:
        return False
    if doctrine_fit.updated_at > timezone.now():
        return False
    fit = json.loads(doctrine_fit.fit)
    price = Decimal(0.0)
    try:
        p = ItemPrice.objects.get(item_id=fit['ship']['ship_id'])
    except ItemPrice.DoesNotExist:
        p = ItemPrice()
        p.item = InvType.objects.get(pk=fit['ship']['ship_id'])
        p.update_price(force=True)
    p.update_price(force=True)
    price += p.price
    for m in fit['modules']:
        try:
            p = ItemPrice.objects.get(item_id=m['id'])
        except ItemPrice.DoesNotExist:
            p = ItemPrice()
            p.item = InvType.objects.get(pk=m['id'])
            p.update_price(force=True)
        p.update_price(force=True)
        price += p.price
    for d in fit['drones']:
        try:
            p = ItemPrice.objects.get(item_id=d['id'])
        except ItemPrice.DoesNotExist:
            p = ItemPrice()
            p.item = InvType.objects.get(pk=m['id'])
            p.update_price(force=True)
        p.update_price(force=True)
        price += (p.price * d['amount'])
    doctrine_fit.price = price
    doctrine_fit.save()


# TODO: Make it so that it updates more than one price
@task()
def update_price_item(item_id):
    item = ItemPrice.objects.get(pk=item_id)
    item.update_price(force=True)
    return item.price