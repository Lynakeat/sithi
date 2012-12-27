from django.core import serializers
from django.http import HttpResponse

from activebuys.apps.deals.models import Deal

def widget(request):
    callback = request.GET['callback']
    
    queryset = Deal.active.all()
    
    # Serialize the queryset in JSON
    json_data = serializers.serialize("json", queryset, indent=4, extras=('first_image',))

    # Convert to JSONP
    jsonp_data = "%s(%s)" % (callback, json_data)
    return HttpResponse(jsonp_data, mimetype="application/json")