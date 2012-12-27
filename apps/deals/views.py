from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template import loader

from activebuys.apps.utils.views import render_to, render_json
from activebuys.apps.deals.models import Deal
from activebuys.apps.deals.forms import get_build_deal_form
from activebuys.apps.widget.models import Widget


@render_to('deals/detail.html')
def detail(request, slug=None):
    """If `slug` == None get nearest active deal"""
    try:
        if slug:
            obj = Deal.objects.get(slug=slug)
        else:
            objs = Deal.active.filter(home_page=True).order_by('-start_time')
            if objs:
                obj = objs[0]
            else:
                obj = Deal.active.all()[0]
    except (Deal.DoesNotExist, IndexError):
        raise Http404

    # Track widgets
    if request.GET.has_key('wid'):
        api_key = request.GET['wid']
        request.session['wid'] = api_key
        try:
            widget = Widget.objects.get(api_key=api_key)
            widget.view_count += 1
            widget.save()
        except:
            pass
    return {'object': obj}


@login_required
@render_to('deals/buy.html')
def buy(request, slug):
    obj = get_object_or_404(Deal.allowed, slug=slug)
    FormClass = get_build_deal_form(obj, request.user, request.session)
    if request.method == "POST":
        form = FormClass(request.POST)
        if form.is_valid():
            form.save_all()
            return redirect(obj.get_absolute_url() + '#open-cart')
    else:
        form = FormClass(initial={'is_gift': 'gift' in request.GET})
    return {'object': obj, 'form': form}


@render_json
def ajax_past_deals(request):
    rendered = loader.render_to_string('deals/ajax_past_deals.html', {})
    return {'html': rendered}
