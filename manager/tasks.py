import datetime
import logging
from decimal import Decimal
from huey.djhuey import task
from django.utils import timezone
import eveapi
from fwmazon.redisevecache import RedisEveAPICacheHandler
from evejournal import EveJournal
from checkout.models import Payment, MONEY_RECEIVED
from eve.models import APIKey, CorpWallet, CorpWalletJournalEntry, ItemPrice
from shop.models import DoctrineFit
l = logging.getLogger('fwmazon')


# TODO: Add ammo support, and we can do better
@task()
def update_fit(fit_id):
    l.info('Starting update_fit task DoctrineFit#%s' %
           fit_id, extra={'fit_id': fit_id})
    try:
        doctrine_fit = DoctrineFit.objects.get(pk=fit_id)
    except DoctrineFit.DoesNotExist:
        return False
    price = Decimal(0.0)
    for element in doctrine_fit.elements.all():
        price += (element.get_price() * element.amount)
    doctrine_fit.status = 1
    doctrine_fit.price = price
    doctrine_fit.save()
    l.info('Ended update_fit task DoctrineFit#%s' %
           fit_id, extra={'fit_id': fit_id})


# TODO: Make it so that it updates more than one price
@task()
def update_price_item(item_ids=[]):
    l.info('Starting update_price_item', extra={'items': item_ids})
    for item_id in item_ids:
        item = ItemPrice.objects.get(pk=item_id)
        item.update_price(force=True)
        return item.price


@task()
def process_journal():
    l.info('Starting process_journal')
    wallets = CorpWallet.objects.all()
    for wallet in wallets:
        l.info('Processing wallet#%s' % wallet.account_key)
        journal = EveJournal(wallet.account_key)
        for page in journal:
            if page is None:
                break
            for transaction in page:
                try:
                    entry = CorpWalletJournalEntry.objects.get(
                        ref_id=transaction.refID)
                except CorpWalletJournalEntry.DoesNotExist:
                    date = timezone.make_aware(
                        datetime.datetime.utcfromtimestamp(transaction.date), timezone.utc)
                    entry_data = {
                        'wallet': wallet,
                        'transaction_date': date,
                        'ref_type_id': transaction.refTypeID,
                        'ref_id': transaction.refID,
                        'sender_name': transaction.ownerName1,
                        'amount': Decimal(transaction.amount),
                        'reason': transaction.reason,
                    }
                    entry = CorpWalletJournalEntry(**entry_data)
                    entry.save()
                    if entry.ref_type_id == 10:
                        process_transaction.schedule(args=(entry.id,), delay=5)


@task()
def process_transaction(entry_id):
    l.info('Starting process_transaction',
           extra={'transaction': entry_id})
    try:
        transaction = CorpWalletJournalEntry.objects.get(pk=entry_id)
    except CorpWalletJournalEntry.DoesNotExist:
        raise CorpWalletJournalEntry.DoesNotExist
    reason = transaction.reason.replace(' ', '').rstrip('\n')[5:]
    try:
        payment = Payment.objects.get(key=reason)
    except Payment.DoesNotExist:
        return
    if payment.status == MONEY_RECEIVED or transaction.amount != payment.order.get().total_price:
        return
    payment.status = MONEY_RECEIVED
    payment.transaction = transaction
    payment.save()
    l.info('Transaction processed', extra={'transaction': entry_id})


@task()
def update_wallets():
    l.info('Starting update_wallets')
    try:
        api_key = APIKey.objects.get(pk=2338850)
    except APIKey.DoesNotExist:
        l.error('Could not find api key to update wallets')
        raise APIKey.DoesNotExist
    api = eveapi.EVEAPIConnection(cacheHandler=RedisEveAPICacheHandler(debug=True)).auth(
        keyID=api_key.id, vCode=api_key.vcode)
    balance = api.corp.AccountBalance()
    for account in balance.accounts:
        try:
            wallet = CorpWallet.objects.get(wallet_id=account.accountID)
        except CorpWallet.DoesNotExist:
            wallet_data = {
                'wallet_id': account.accountID, 'account_key': account.accountKey,
                'apikey': api_key, 'name': 'Not named #%s' % account.accountID}
            wallet = CorpWallet(**wallet_data)
        wallet.balance = Decimal(account.balance)
        wallet.save()
        l.info('Updated Wallet#%s' % wallet.account_key)
    l.info('Finished updating wallets')
