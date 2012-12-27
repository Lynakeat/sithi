from activebuys.apps.utils.views import render_json
from activebuys.apps.companies.models import CompanyAddress

@render_json
def company_addressajaxlist(request):
    id = request.GET.get('id')
    items = {}
    if id:
        items = CompanyAddress.objects.filter(company__id=int(id)).values('id', 'place')
        items = dict((i['id'], i['place']) for i in items)
    return {'items': items}

