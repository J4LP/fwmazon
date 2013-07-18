# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('auth_user', 'account_user')
        db.rename_table('auth_user_groups', 'account_user_groups')
        db.rename_table('auth_user_permissions', 'account_user_permissions')

    def backwards(self, orm):
        db.rename_table('account_user', 'auth_user')
        db.rename_table('account_user_groups', 'auth_user_groups')
        db.rename_table('account_user_permissions', 'auth_user_permissions')

    models = {
        
    }

    complete_apps = ['account']