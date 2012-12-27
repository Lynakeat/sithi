import ho.pisa as pisa
import cStringIO as StringIO
from django.template.loader import render_to_string
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.core.files.base import ContentFile, File

def generate_voucher(obj):
    """ Return StringIO object that contains generated PDF body """
    context = dict(
        voucher=obj,
        accountdeal=obj.accountdeal,
        user=obj.accountdeal.account,
        deal=obj.accountdeal.deal,
        MEDIA_ROOT=settings.MEDIA_ROOT
    )   
    #body = render_to_string("vouchers/pdf.html", context)
    #result = StringIO.StringIO()
    #pisa.CreatePDF(body, result)
    
    #pisa.showLogging(debug=True)
    template = get_template("vouchers/pdf.html")
    html = template.render(Context(context))
    #print html
    temp_file = StringIO.StringIO()
    pisa.CreatePDF(StringIO.StringIO(html.encode("UTF-8")), temp_file)
    return temp_file
