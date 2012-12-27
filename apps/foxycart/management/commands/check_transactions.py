import urllib
from xml.dom.minidom import parseString

from django.core.management.base import NoArgsCommand
from django.conf import settings

from activebuys.apps.foxycart.views import create_order_from_datafeed
import activebuys.apps.foxycart as foxycart

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        params = {
            'data_is_fed_filter': 0
        }
        xml_data = foxycart.api_call('transaction_list', **params)
        data = foxycart.FoxyData.from_str(xml_data)

        for transaction in data.transactions:
            trans_id = create_order_from_datafeed(transaction)
        
            if trans_id:
                # Mark as fed from FoxyCart
                params = {
                   'data_is_fed': 1,
                    'transaction_id': trans_id
                }
                foxycart.api_call('transaction_modify', **params)

