# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SubscribeLocation'
        db.create_table('accounts_subscribelocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('cmonitor_name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('accounts', ['SubscribeLocation'])

        # Adding model 'Account'
        db.create_table('accounts_account', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('referred_email', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('confirm_email_code', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('foxycart_customer_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('accounts', ['Account'])

        # Adding M2M table for field subscribe_location on 'Account'
        db.create_table('accounts_account_subscribe_location', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm['accounts.account'], null=False)),
            ('subscribelocation', models.ForeignKey(orm['accounts.subscribelocation'], null=False))
        ))
        db.create_unique('accounts_account_subscribe_location', ['account_id', 'subscribelocation_id'])

        # Adding model 'AccountDeal'
        db.create_table('accounts_accountdeal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=10)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Account'])),
            ('deal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deals.Deal'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companies.CompanyAddress'])),
            ('nonprofit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companies.NonProfit'], null=True, blank=True)),
            ('is_gift', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name_to', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('name_from', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('surprise', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email_to', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fcc_session_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('accounts', ['AccountDeal'])

        # Adding model 'Order'
        db.create_table('accounts_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('transaction_id', self.gf('django.db.models.fields.BigIntegerField')(max_length=255)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Account'])),
            ('total', self.gf('django.db.models.fields.FloatField')()),
            ('receipt_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('accounts', ['Order'])

        # Adding M2M table for field deals on 'Order'
        db.create_table('accounts_order_deals', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('order', models.ForeignKey(orm['accounts.order'], null=False)),
            ('accountdeal', models.ForeignKey(orm['accounts.accountdeal'], null=False))
        ))
        db.create_unique('accounts_order_deals', ['order_id', 'accountdeal_id'])

        # Adding model 'Data'
        db.create_table('accounts_data', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('accounts', ['Data'])

        # Adding model 'RestorePasswordRequest'
        db.create_table('accounts_restorepasswordrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Account'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('accounts', ['RestorePasswordRequest'])


    def backwards(self, orm):
        
        # Deleting model 'SubscribeLocation'
        db.delete_table('accounts_subscribelocation')

        # Deleting model 'Account'
        db.delete_table('accounts_account')

        # Removing M2M table for field subscribe_location on 'Account'
        db.delete_table('accounts_account_subscribe_location')

        # Deleting model 'AccountDeal'
        db.delete_table('accounts_accountdeal')

        # Deleting model 'Order'
        db.delete_table('accounts_order')

        # Removing M2M table for field deals on 'Order'
        db.delete_table('accounts_order_deals')

        # Deleting model 'Data'
        db.delete_table('accounts_data')

        # Deleting model 'RestorePasswordRequest'
        db.delete_table('accounts_restorepasswordrequest')


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account', '_ormbases': ['auth.User']},
            'confirm_email_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'foxycart_customer_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'referred_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subscribe_location': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['accounts.SubscribeLocation']", 'symmetrical': 'False'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'accounts.accountdeal': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'AccountDeal'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'deal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deals.Deal']"}),
            'email_to': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fcc_session_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_gift': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['companies.CompanyAddress']"}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name_from': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_to': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nonprofit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['companies.NonProfit']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '10'}),
            'surprise': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'accounts.data': {
            'Meta': {'object_name': 'Data'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'accounts.order': {
            'Meta': {'object_name': 'Order'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'deals': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['accounts.AccountDeal']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receipt_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'total': ('django.db.models.fields.FloatField', [], {}),
            'transaction_id': ('django.db.models.fields.BigIntegerField', [], {'max_length': '255'})
        },
        'accounts.restorepasswordrequest': {
            'Meta': {'object_name': 'RestorePasswordRequest'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'accounts.subscribelocation': {
            'Meta': {'object_name': 'SubscribeLocation'},
            'cmonitor_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'companies.company': {
            'Meta': {'object_name': 'Company'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'companies.companyaddress': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'CompanyAddress'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['companies.Company']"}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'})
        },
        'companies.nonprofit': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'NonProfit'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'deals.background': {
            'Meta': {'object_name': 'Background'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'deals.deal': {
            'Meta': {'ordering': "['end_time']", 'object_name': 'Deal'},
            'allow_gifts': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'background': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['deals.Background']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['companies.Company']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'expire_date': ('django.db.models.fields.DateField', [], {}),
            'fine_print': ('django.db.models.fields.TextField', [], {}),
            'gift_limit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'home_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['companies.CompanyAddress']", 'symmetrical': 'False'}),
            'nonprofit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['companies.NonProfit']", 'null': 'True', 'blank': 'True'}),
            'open_after_expire': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'original_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'per_user': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'db_index': 'True'}),
            'sold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'total_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['accounts']
