from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal as d
import xml.etree.ElementTree as ET
from time import sleep
import requests
from datetime import datetime, timedelta


class APIKey(models.Model):
    """
    Simple model for apikey storage
    """
    id = models.IntegerField(primary_key=True, editable=True)
    vcode = models.CharField(max_length=64, editable=True)
    user = models.OneToOneField(User, null=True)


class Character(models.Model):
    """
    Simple model to store character name and id
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    #TODO: Integrate this with update_user.py
    #corporation = models.IntegerField()
    user = models.OneToOneField(User)


class InvMarketGroup(models.Model):
    """
    Market groups are used to group items together in the market browser.

    CCP Table: invMarketGroups
    CCP Primary key: "marketGroupID" smallint(6)
    """
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=300012, blank=True, null=True)
    parent = models.ForeignKey('InvMarketGroup', blank=True, null=True)
    has_items = models.BooleanField(default=True)
    icon_id = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Market Group'
        verbose_name_plural = 'Market Groups'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    def full_name(self, delimiter='/'):
        """
        Return a full name, including parents, recursively.
        """
        if self.parent:
            return self.parent.full_name() + delimiter + self.name
        else:
            return self.name


class InvCategory(models.Model):
    """
    Inventory categories are the top level classification for all items, be
    it planets, moons, modules, ships, or any other entity within the game
    that physically exists.

    CCP Table: invCategories
    CCP Primary key: "categoryID" tinyint(3)
    """
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    is_published = models.BooleanField(default=True)
    icon_id = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory Category'
        verbose_name_plural = 'Inventory Categories'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


class InvGroup(models.Model):
    """
    Inventory groups are a further sub-classification within an
    InvCategory. For example, the 'MapRegion' inventory group's
    category is 'Celestial'.

    CCP Table: invGroups
    CCP Primary key: "groupID" smallint(6)
    """
    id = models.IntegerField(unique=True, primary_key=True)
    category = models.ForeignKey(InvCategory, blank=True, null=True)
    name = models.CharField(max_length=150)
    description = models.TextField()
    icon_id = models.IntegerField(blank=True, null=True)
    use_base_price = models.BooleanField(default=False)
    allow_manufacture = models.BooleanField(default=True)
    allow_recycle = models.BooleanField(default=True)
    allow_anchoring = models.BooleanField(default=False)
    is_anchored = models.BooleanField(default=False)
    is_fittable_non_singleton = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory Group'
        verbose_name_plural = 'Inventory Groups'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


class InvType(models.Model):
    """
    Inventory types are generally objects that can be carried in your
    inventory (with the exception of suns, moons, planets, etc.) These are mostly
    market items, along with some basic attributes of each that are common
    to all items.

    CCP Table: invTypes
    CCP Primary key: "typeID" smallint(6)
    """
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    group = models.ForeignKey(InvGroup, blank=True, null=True)
    market_group = models.ForeignKey(InvMarketGroup, blank=True, null=True)
    mass = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    capacity = models.FloatField(blank=True, null=True)
    portion_size = models.IntegerField(blank=True, null=True)
    base_price = models.FloatField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    chance_of_duplicating = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Inventory Type'
        verbose_name_plural = 'Inventory Types'

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return "Inventory Type #%d" % self.id

    def __str__(self):
        return self.__unicode__()
        

class ItemPrice(models.Model):
    price = models.DecimalField(max_digits=30, decimal_places=2, default=d(0.00))
    item = models.ForeignKey(InvType, related_name='price')
    expires = models.DateTimeField()

    def update_price(self, force=False):
        if self.expires is None or self.expires < timezone.now() or force is True:
            price = 0.0
            try:
                r = requests.get('http://api.eve-central.com/api/marketstat?typeid=' + str(self.item.id) + '&usesystem=30000142')
                root = ET.fromstring(r.text)
                all = root[0][0].find('all')
                price = all.find('avg').text
                sleep(1)
            except:
                pass
            self.price = Decimal(price)
            self.save()
        return

    def save(self, *args, **kwargs):
        d = timedelta(days=1)
        self.expires = timezone.now() + d
        super(ItemPrice, self).save()


class WalletMixin(models.Model):
    wallet_id = models.IntegerField(primary_key=True)
    account_key = models.IntegerField(default=1000)
    apikey = models.ForeignKey(APIKey)

    class Meta:
        abstract = True


class CorpWallet(WalletMixin):
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=30, decimal_places=2, default=d(0.00))


class CorpWalletJournalEntry(models.Model):
    wallet = models.ForeignKey(CorpWallet, related_name='entries')
    transaction_date = models.DateTimeField()
    ref_type_id = models.IntegerField()
    ref_id = models.BigIntegerField()
    sender_name = models.CharField(max_length=65)
    amount = models.DecimalField(max_digits=30, decimal_places=2, default=d(0.00))
    reason = models.CharField(max_length=128)

    class Meta:
        get_latest_by = "transaction_date"
