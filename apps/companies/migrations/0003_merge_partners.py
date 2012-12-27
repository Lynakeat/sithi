# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        """Save a Company record with `is_partner=True` for each Partner, 
        delete the Partner records. Ordering is overridden. """
        sort_order_value = 1
        if orm.Company.objects.count() > 0:
            sort_order_value = orm.Company.objects.all().order_by('-sort_order')[0].sort_order + 1
        for p in orm.Partner.objects.all():
            orm.Company.objects.create(
                                    name=p.name, 
                                    description=p.description, 
                                    logo=p.logo,
                                    website=p.website,
                                    is_partner=True,
                                    sort_order=sort_order_value)
            sort_order_value+=1
        orm.Partner.objects.all().delete()


    def backwards(self, orm):
        """Save a Partner record for each Company with `is_partner=True`, delete 
        those Companies.  Ordering is overridden. May not work for Companies with addresses.
        It is not anticipated to need this reverse method."""
        sort_order_value = 1
        if orm.Partner.objects.count() > 0:
            sort_order_value = orm.Partner.objects.all().order_by('-sort_order')[0].sort_order + 1
        for c in orm.Company.objects.filter(is_partner=True):
            orm.Partner.objects.create(
                                    name=c.name, 
                                    description=c.description, 
                                    logo=c.logo,
                                    website=c.website,
                                    sort_order=sort_order_value)
            sort_order_value+=1
        orm.Company.objects.filter(is_partner=True).delete()


    models = {
        'companies.company': {
            'Meta': {'object_name': 'Company'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_partner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
        'companies.partner': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Partner'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['companies']
