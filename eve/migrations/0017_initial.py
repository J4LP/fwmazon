# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'APIKey'
        db.create_table(u'eve_apikey', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('vcode', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['account.User'], unique=True, null=True)),
        ))
        db.send_create_signal(u'eve', ['APIKey'])

        # Adding model 'Character'
        db.create_table(u'eve_character', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['account.User'], unique=True)),
        ))
        db.send_create_signal(u'eve', ['Character'])

        # Adding model 'InvMarketGroup'
        db.create_table(u'eve_invmarketgroup', (
            ('id', self.gf('django.db.models.fields.IntegerField')(unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=300012, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve.InvMarketGroup'], null=True, blank=True)),
            ('has_items', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('icon_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'eve', ['InvMarketGroup'])

        # Adding model 'InvCategory'
        db.create_table(u'eve_invcategory', (
            ('id', self.gf('django.db.models.fields.IntegerField')(unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('icon_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'eve', ['InvCategory'])

        # Adding model 'InvGroup'
        db.create_table(u'eve_invgroup', (
            ('id', self.gf('django.db.models.fields.IntegerField')(unique=True, primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve.InvCategory'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('icon_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('use_base_price', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_manufacture', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('allow_recycle', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('allow_anchoring', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_anchored', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_fittable_non_singleton', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'eve', ['InvGroup'])

        # Adding model 'InvType'
        db.create_table(u'eve_invtype', (
            ('id', self.gf('django.db.models.fields.IntegerField')(unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve.InvGroup'], null=True, blank=True)),
            ('market_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve.InvMarketGroup'], null=True, blank=True)),
            ('mass', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('volume', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('capacity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('portion_size', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('base_price', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('chance_of_duplicating', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'eve', ['InvType'])

        # Adding model 'ItemPrice'
        db.create_table(u'eve_itemprice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=30, decimal_places=2)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='price', to=orm['eve.InvType'])),
            ('expires', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'eve', ['ItemPrice'])

        # Adding model 'CorpWallet'
        db.create_table(u'eve_corpwallet', (
            ('wallet_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('account_key', self.gf('django.db.models.fields.IntegerField')(default=1000)),
            ('apikey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eve.APIKey'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=30, decimal_places=2)),
        ))
        db.send_create_signal(u'eve', ['CorpWallet'])

        # Adding model 'CorpWalletJournalEntry'
        db.create_table(u'eve_corpwalletjournalentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wallet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['eve.CorpWallet'])),
            ('transaction_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('ref_type_id', self.gf('django.db.models.fields.IntegerField')()),
            ('ref_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('sender_name', self.gf('django.db.models.fields.CharField')(max_length=65)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=30, decimal_places=2)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'eve', ['CorpWalletJournalEntry'])


    def backwards(self, orm):
        # Deleting model 'APIKey'
        db.delete_table(u'eve_apikey')

        # Deleting model 'Character'
        db.delete_table(u'eve_character')

        # Deleting model 'InvMarketGroup'
        db.delete_table(u'eve_invmarketgroup')

        # Deleting model 'InvCategory'
        db.delete_table(u'eve_invcategory')

        # Deleting model 'InvGroup'
        db.delete_table(u'eve_invgroup')

        # Deleting model 'InvType'
        db.delete_table(u'eve_invtype')

        # Deleting model 'ItemPrice'
        db.delete_table(u'eve_itemprice')

        # Deleting model 'CorpWallet'
        db.delete_table(u'eve_corpwallet')

        # Deleting model 'CorpWalletJournalEntry'
        db.delete_table(u'eve_corpwalletjournalentry')


    models = {
        u'account.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_contractor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_manager': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'eve.apikey': {
            'Meta': {'object_name': 'APIKey'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['account.User']", 'unique': 'True', 'null': 'True'}),
            'vcode': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'eve.character': {
            'Meta': {'object_name': 'Character'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['account.User']", 'unique': 'True'})
        },
        u'eve.corpwallet': {
            'Meta': {'object_name': 'CorpWallet'},
            'account_key': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'apikey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eve.APIKey']"}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '30', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'wallet_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        u'eve.corpwalletjournalentry': {
            'Meta': {'object_name': 'CorpWalletJournalEntry'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '30', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'ref_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'ref_type_id': ('django.db.models.fields.IntegerField', [], {}),
            'sender_name': ('django.db.models.fields.CharField', [], {'max_length': '65'}),
            'transaction_date': ('django.db.models.fields.DateTimeField', [], {}),
            'wallet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['eve.CorpWallet']"})
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
        u'eve.itemprice': {
            'Meta': {'object_name': 'ItemPrice'},
            'expires': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'price'", 'to': u"orm['eve.InvType']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '30', 'decimal_places': '2'})
        }
    }

    complete_apps = ['eve']