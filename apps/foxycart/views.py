import urllib
import hashlib
import traceback

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required

from activebuys.apps.accounts.models import AccountDeal, Account, Order, Data
from activebuys.apps.accounts.mails import send_emails_on_order_creation
from activebuys.apps.widget.models import Widget

from activebuys.apps.foxycart import FoxyData

def create_order_from_datafeed(transaction):
    """ Foxycart transaction to Order instance """
    transaction_id = transaction.id
    transaction_date = transaction.transaction_date
    customer_id = int(transaction.get('customer_id'))
    order_total = transaction.get('order_total')
    receipt_url = transaction.get('receipt_url')
    transaction_details = transaction.transaction_details

    try:
        account = Account.objects.get(foxycart_customer_id=customer_id)
        try:
            order = Order.objects.get(transaction_id=transaction_id)
        except Order.DoesNotExist:
            order = Order(transaction_id=transaction_id,
                          date=transaction_date,
                          total=order_total,
                          receipt_url=receipt_url,
                          account=account)
            order.save()
            # collect user_deals that client had added to cart
            for i in transaction_details.items:
                quantity = i.get('product_quantity')
                id = i.options.get('id')
                qs = AccountDeal.objects.all_new().\
                                 filter(account__foxycart_customer_id=customer_id)
                for i in qs.filter(deal__id=id)[:quantity]:
                    i.status = AccountDeal.PAID
                    i.save()
                    order.deals.add(i)
            send_emails_on_order_creation(order)
            
        # Track widget referrals
        if transaction.custom_fields.get('widget_id'):
            widget = Widget.objects.get(api_key=transaction.custom_fields.get('widget_id').value)
            widget.orders.add(order)
            widget.save()
    except Account.DoesNotExist:
        return False
        
    return transaction_id

@csrf_exempt
def datafeed(request):
    if request.POST and request.POST.has_key('FoxyData'):
        if request.POST.has_key('testing'):
            data = FoxyData.from_str(request.POST['FoxyData'])
        else:
            data = FoxyData.from_crypted_str(urllib.unquote_plus(request.POST['FoxyData']),
                                                             settings.FOXYCART_API_KEY)
        data_object = Data(data=data)
        data_object.save()
        # IMPORTANT: unquote_plus is necessary for the non-ASCII binary that FoxyCart sends.
        for transaction in data.transactions:
            create_order_from_datafeed(transaction)
        return HttpResponse('foxy')
    return HttpResponseForbidden('Unauthorized request.')

@login_required
def sso(request):
    """ Foxycart shared authentication """
    #url = "https://%s.foxycart.com/checkout" % settings.FOXYCART_SHOP_NAME
    url = settings.FOXYCART_URL + 'checkout'

    timestamp = request.GET.get('timestamp')
    fcsid = request.GET.get('fcsid')

    if timestamp and fcsid:
        customer_id = str(request.user.foxycart_customer_id)
        timestamp = str(int(timestamp) + (60*30))
        hash = hashlib.sha1()
        hash.update('|'.join([customer_id, timestamp, settings.FOXYCART_API_KEY])),
        params = {
            'fc_auth_token': hash.hexdigest(),
            'fcsid': fcsid,
            'fc_customer_id': customer_id,
            'timestamp': timestamp,
        }
        return HttpResponseRedirect('?'.join([url, urllib.urlencode(params)]))

    return HttpResponseRedirect(url)

