# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Order.total_price'
        db.delete_column(u'checkout_order', 'total_price')

        # Deleting field 'Order.shipping_fee'
        db.delete_column(u'checkout_order', 'shipping_fee')

        # Adding field 'Order.volume'
        db.add_column(u'checkout_order', 'volume',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=15, decimal_places=2, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Order.total_price'
        db.add_column(u'checkout_order', 'total_price',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=15, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'Order.shipping_fee'
        db.add_column(u'checkout_order', 'shipping_fee',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=15, decimal_places=2, blank=True),
                      keep_default=False)

        # Deleting field 'Order.volume'
        db.delete_column(u'checkout_order', 'volume')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'checkout.order': {
            'Meta': {'object_name': 'Order'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'elements_price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shipping_destination': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkout.ShippingDestination']"}),
            'to_be_fitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'})
        },
        u'checkout.orderelement': {
            'Meta': {'object_name': 'OrderElement'},
            'doctrine_fit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.DoctrineFit']"}),
            'element_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eve.InvType']"}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'elements'", 'to': u"orm['checkout.Order']"})
        },
        u'checkout.shippingdestination': {
            'Meta': {'object_name': 'ShippingDestination'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delay': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'shipping_cost': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'eve.invcategory': {
            'Meta': {'ordering': "['id']", 'object_name': 'InvCategory'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'icon_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'eve.invgroup': {
            'Meta': {'ordering': "['id']", 'object_name': 'InvGroup'},
            'allow_anchoring': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_manufacture': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'allow_recycle': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eve.InvCategory']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'icon_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_anchored': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_fittable_non_singleton': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'use_base_price': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'eve.invmarketgroup': {
            'Meta': {'ordering': "['id']", 'object_name': 'InvMarketGroup'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '300012', 'null': 'True', 'blank': 'True'}),
            'has_items': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'icon_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eve.InvMarketGroup']", 'null': 'True', 'blank': 'True'})
        },
        u'eve.invtype': {
            'Meta': {'ordering': "['id']", 'object_name': 'InvType'},
            'base_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'capacity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'chance_of_duplicating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eve.InvGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'market_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eve.InvMarketGroup']", 'null': 'True', 'blank': 'True'}),
            'mass': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'portion_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'shop.doctrinefit': {
            'Meta': {'object_name': 'DoctrineFit'},
            'bought': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'fit': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '15', 'decimal_places': '2', 'blank': 'True'}),
            'ship': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eve.InvType']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['checkout']