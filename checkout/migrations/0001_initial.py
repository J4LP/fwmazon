# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShippingDestination'
        db.create_table(u'checkout_shippingdestination', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('shipping_cost', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=15, decimal_places=2, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('delay', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'checkout', ['ShippingDestination'])


    def backwards(self, orm):
        # Deleting model 'ShippingDestination'
        db.delete_table(u'checkout_shippingdestination')


    models = {
        u'checkout.shippingdestination': {
            'Meta': {'object_name': 'ShippingDestination'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delay': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shipping_cost': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'})
        }
    }

    complete_apps = ['checkout']