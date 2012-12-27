# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Deal'
        db.create_table('deals_deal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('original_price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('expire_date', self.gf('django.db.models.fields.DateField')()),
            ('open_after_expire', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('total_number', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('sold', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('per_user', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('gift_limit', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companies.Company'])),
            ('nonprofit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companies.NonProfit'], null=True, blank=True)),
            ('fine_print', self.gf('django.db.models.fields.TextField')()),
            ('background', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deals.Background'])),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_gifts', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('home_page', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('deals', ['Deal'])

        # Adding M2M table for field locations on 'Deal'
        db.create_table('deals_deal_locations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('deal', models.ForeignKey(orm['deals.deal'], null=False)),
            ('companyaddress', models.ForeignKey(orm['companies.companyaddress'], null=False))
        ))
        db.create_unique('deals_deal_locations', ['deal_id', 'companyaddress_id'])

        # Adding model 'Picture'
        db.create_table('deals_picture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('deal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='deal_photos', to=orm['deals.Deal'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('deals', ['Picture'])

        # Adding model 'Background'
        db.create_table('deals_background', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('deals', ['Background'])


    def backwards(self, orm):
        # Deleting model 'Deal'
        db.delete_table('deals_deal')

        # Removing M2M table for field locations on 'Deal'
        db.delete_table('deals_deal_locations')

        # Deleting model 'Picture'
        db.delete_table('deals_picture')

        # Deleting model 'Background'
        db.delete_table('deals_background')


    models = {
        'companies.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'featured_location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['companies.CompanyAddress']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'companies.company': {
            'Meta': {'object_name': 'Company'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'enable_courses': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enable_pricing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enable_products': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enable_reviews': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_partner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notification_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'companies.companyaddress': {
            'Meta': {'object_name': 'CompanyAddress'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['companies.Category']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['companies.Company']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'facebook_profile': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hours': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'default': "'TN'", 'max_length': '2'}),
            'subcategories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['companies.SubCategory']", 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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
        'companies.subcategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'SubCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['companies.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
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
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'sold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'total_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'deals.picture': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Picture'},
            'deal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deal_photos'", 'to': "orm['deals.Deal']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['deals']