# -*- coding: utf-8 -*-

import eveapi
from fwmazon import settings
from fwmazon.redisevecache import RedisEveAPICacheHandler
import redis
from time import sleep


class EveJournal(object):
    def __init__(self, wallet):
        try:
            self.key_id = settings.FW_KEY_ID
            self.vcode = settings.FW_VCODE
            self.account_key = wallet
        except NameError:
            raise NameError('Please fill in your settings file')
        self.api = eveapi.EVEAPIConnection(cacheHandler=RedisEveAPICacheHandler(debug=True)).auth(keyID=self.key_id, vCode=self.vcode)
        self.batch_length = 2560
        self.latest_length = None
        self.oldest_transaction = None
        try:
            self.redis = redis.StrictRedis()
            self.db_oldest_transaction = self.redis.get('evejournal:last_transaction')
            if self.db_oldest_transaction is not None or self.db_oldest_transaction != 'None':
                self.db_oldest_transaction = int(self.db_oldest_transaction)
        except redis.exceptions.ConnectionError:
            raise redis.exceptions.ConnectionError('Please ensure you have redis up and running')

    def __iter__(self):
        return self

    def reset(self):
        self.redis.set('evejournal:last_transaction', self.oldest_transaction)
        self.db_oldest_transaction = self.oldest_transaction
        self.oldest_transaction = None
        self.latest_length = None

    def next(self):
        # We don't want to get banned from the api :ccp:
        sleep(1)
        # Check by length
        if (self.latest_length and self.batch_length) and (self.latest_length < self.batch_length):
            self.reset()
            raise StopIteration
        # Check by db last transaction
        if self.db_oldest_transaction and self.oldest_transaction and (self.oldest_transaction <= self.db_oldest_transaction):
            self.reset()
            raise StopIteration

        # API Request
        try:
            if self.oldest_transaction is None:
                transactions = self.api.corp.WalletJournal(accountKey=self.account_key, rowCount=self.batch_length).entries
            else:
                transactions = self.api.corp.WalletJournal(accountKey=self.account_key, rowCount=self.batch_length, fromID=self.oldest_transaction).entries
        except eveapi.Error, e:
            # TODO : Log error
            return None

        # If no transactions, there isn't any anymore
        if len(transactions) == 0:
            self.reset()
            raise StopIteration

        # Sorting and storing
        transactions.SortBy('date')
        self.latest_length = len(transactions)
        self.oldest_transaction = transactions[0]['refID']

        return transactions