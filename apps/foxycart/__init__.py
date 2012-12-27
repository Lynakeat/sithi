"""
Utilities for decrypting and parsing a FoxyCart datafeed.
"""
import urllib
from xml.dom.minidom import parseString
from datetime import datetime

from django.conf import settings
from django.utils import simplejson as json
from django.utils.datastructures import SortedDict


class Cart(object):
    base_url = settings.FOXYCART_URL+'cart?output=json'

    def __init__(self, fcc_session_id):
        if '&fcsid=' not in fcc_session_id:
            fcc_session_id = '&fcsid=' + fcc_session_id
        self.fcc_session_id = fcc_session_id
        self.base_url = self.base_url + fcc_session_id
        self.content = self.view_cart()

    def _base_action(self, params):
        url = '&'.join([self.base_url, urllib.urlencode(params)])
        self.content = json.loads(urllib.urlopen(url).read())
        return self.content

    def view_cart(self):
        """ return cart content """
        url_dict = {'cart': 'view'}
        return self._base_action(url_dict)

    def add_to_cart(self, deal, quantity=1):
        """ add item to foxycart and return foxycart product ID """
        url_dict = SortedDict() # for correct order on checkout page
        url_dict['name'] = unicode(deal.deal)
        url_dict['price'] = deal.deal.price
        url_dict['quantity'] = quantity
        url_dict['id'] = deal.deal.id
        url_dict['Non-Profit'] = deal.nonprofit.name
        if deal.is_gift:
            url_dict['To'] = deal.name_to
            if not deal.surprise:
                url_dict['Email to'] = deal.email_to
            url_dict['Location'] = unicode(deal.location)
        if deal.widget_id:
            url_dict['h:widget_id'] = deal.widget_id
        self._base_action(url_dict)

    def update_cart(self, deal,  quantity):
        """ update quanity in cart """
        product = self.get_product(deal)
        if not product:
            return
        url_dict = {
            'cart': 'update',
            'id': product['id'],
            'quantity': quantity
        }
        self._base_action(url_dict)

    def clean_cart(self):
        url_dict = {
            'cart': 'empty',
        }
        self._base_action(url_dict)

    def get_product(self, deal):
        result = None
        for product in self.content['products']:
            if int(product['options']['id']) == deal.deal.id:
                result = product
                break
        return result


# Thanks, Wikipedia: http://en.wikipedia.org/wiki/RC4#Implementation
class ARC4(object):
    def __init__(self, key = None):
        self.state = range(256) # Initialize state array with values 0 .. 255
        self.x = self.y = 0 # Our indexes. x, y instead of i, j
 
        if key is not None:
            self.init(key)
 
    # KSA
    def init(self, key):
        for i in range(256):
            self.x = (ord(key[i % len(key)]) + self.state[i] + self.x) & 0xFF
            self.state[i], self.state[self.x] = self.state[self.x], self.state[i]
        self.x = 0
 
    # PRGA
    def crypt(self, input):
        output = [None]*len(input)
        for i in xrange(len(input)):
            self.x = (self.x + 1) & 0xFF
            self.y = (self.state[self.x] + self.y) & 0xFF
            self.state[self.x], self.state[self.y] = self.state[self.y], self.state[self.x]
            r = self.state[(self.state[self.x] + self.state[self.y]) & 0xFF]
            output[i] = chr(ord(input[i]) ^ r)
        return ''.join(output)


class FoxyData(object):
    DateFmt = '%Y-%m-%d'
    DateTimeFmt = '%Y-%m-%d %H:%M:%S'

    class BaseElement(object):
        def get(self, key_name):
            def extract_kv_node(node, key_name):
                el = node.getElementsByTagName(key_name)
                return len(el) > 0 and el[0].firstChild and el[0].firstChild.data or ''
            return extract_kv_node(self.node, key_name)

        class Meta:
            abstract = True

    class Element(BaseElement):
        def __init__(self, node):
            self.node = node

    class Transaction(BaseElement):
        """ Transactions -> Transaction """
        def __init__(self, node):
            self.node = node

            self.id = self.get('id')
            self.transaction_date = datetime.strptime(self.get('transaction_date'), FoxyData.DateTimeFmt)
            self.custom_fields = FoxyData.CustomFields(self.node.getElementsByTagName('custom_fields'))
            self.transaction_details = FoxyData.TransactionDetails(self.node.getElementsByTagName('transaction_details'))

    class TransactionDetails(BaseElement):
        """ Transaction -> TransactionDetails"""
        def __init__(self, node):
            self.node = node[0]
            self.items = []
            # get all products from this transaction 
            for item in self.node.getElementsByTagName('transaction_detail'):
                self.items.append(FoxyData.Element(item))
                # create options for each product
                options = {}
                options_list = item.getElementsByTagName('transaction_detail_options')[0].\
                                        getElementsByTagName('transaction_detail_option')
                for i in options_list:
                    option = FoxyData.Element(i)                    
                    options[option.get('product_option_name').lower()] = option.get('product_option_value')
                setattr(self.items[-1], 'options', options)

    class CustomFields(dict):
        """ 
            Transaction -> Custom Fields
        """
        def __init__(self, node):
            super(FoxyData.CustomFields, self).__init__()
            for field in node:
                field_obj = FoxyData.CustomField(field)
                self.update({field_obj.name: field_obj})


    class CustomField(BaseElement):
        """ Transaction -> Custom Fields -> Custom Field """
        def __init__(self, node):
            self.node = node
            self.name = self.get('custom_field_name')
            self.value = self.get('custom_field_value')
            self.is_hidden = self.get('custom_field is_hidden')

        def __str_(self):
            return self.name


    def __init__(self, markup):
        self.markup = markup
        self.doc = parseString(self.markup)
        self.transactions = []

        for transaction in self.doc.getElementsByTagName('transaction'):
            self.transactions.append(FoxyData.Transaction(transaction))

    def __str__(self):
        return str(self.markup)

    @classmethod
    def from_str(self, data_str):
        return FoxyData(data_str)

    @classmethod
    def from_crypted_str(self, data_str, crypt_key):
        """
            Given a string containing RC4-crypted FoxyCart datafeed XML and the
            cryptographic key, decrypt the contents and create a FoxyData object
            containing all of the Transactions in the data feed.
        """
        a = ARC4(crypt_key)
        return FoxyData.from_str(a.crypt(data_str))

    def __len__(self):
        return len(self.transactions)


def api_call(command, **params):
    #url = 'https://%s.foxycart.com/api' % settings.FOXYCART_SHOP_NAME
    url = settings.FOXYCART_URL + 'api'
    params.update({
        'api_action': command,
        'api_token': settings.FOXYCART_API_KEY 
    })  
    return urllib.urlopen(url, data=urllib.urlencode(params)).read()

def customer_save_command(email, **params):
    """ Foxycart API call `customer_save`
        return `foxycart_customer_id` 
    """
    params.update({'customer_email': email})
    response = api_call('customer_save', **params)
    fd = FoxyData.from_str(response)
    return int(fd.doc.childNodes[0].getElementsByTagName('customer_id')[0].firstChild.data)
