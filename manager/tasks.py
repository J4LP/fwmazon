from celery import task
from shop.models import DoctrineFit
from django.utils import timezone
import json
from decimal import Decimal
from eve.models import ItemPrice, InvType
from evejournal import EveJournal
import eveapi
from eve.models import APIKey, CorpWallet, CorpWalletJournalEntry
from fwmazon.redisevecache import RedisEveAPICacheHandler
from decimal import Decimal as d
import datetime


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
        price += p.price
    for d in fit['drones']:
        try:
            p = ItemPrice.objects.get(item_id=d['id'])
        except ItemPrice.DoesNotExist:
            p = ItemPrice()
            p.item = InvType.objects.get(pk=m['id'])
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


@task()
def process_journal():
    wallets = CorpWallet.objects.all()
    for wallet in wallets:
        journal = EveJournal(wallet.account_key)
        for page in journal:
            if page is None:
                break
            for transaction in page:
                try:
                    entry = CorpWalletJournalEntry.objects.get(ref_id=transaction.refID)
                except CorpWalletJournalEntry.DoesNotExist:
                    date = datetime.datetime.utcfromtimestamp(transaction.date)
                    entry_data = {
                        'wallet': wallet,
                        'transaction_date': date,
                        'ref_type_id': transaction.refTypeID,
                        'ref_id': transaction.refID,
                        'sender_name': transaction.ownerName1,
                        'amount': d(transaction.amount),
                        'reason': transaction.reason,
                    }
                    entry = CorpWalletJournalEntry(**entry_data)
                    entry.save()
                    if entry.ref_type_id == 10:
                        process_transaction.delay(entry.id)

                        #TODO TIMEZONE ACTIVATE TZINFO WAHTEVER


@task()
def process_transaction(transaction_id):
    raise NotImplementedError


@task()
def update_wallets():
    api_key = APIKey.objects.get(pk=2338850)
    api = eveapi.EVEAPIConnection(cacheHandler=RedisEveAPICacheHandler(debug=True)).auth(keyID=api_key.id, vCode=api_key.vcode)
    balance = api.corp.AccountBalance()
    for account in balance.accounts:
        try:
            wallet = CorpWallet.objects.get(wallet_id=account.accountID)
        except CorpWallet.DoesNotExist:
            wallet_data = {'wallet_id': account.accountID, 'account_key': account.accountKey, 'apikey': api_key, 'name': 'Not named #%s' % account.accountID}
            wallet = CorpWallet(**wallet_data)
        wallet.balance = d(account.balance)
        wallet.save()
