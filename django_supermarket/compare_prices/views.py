from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.conf import settings
from django.db import connection
import json
import datetime

from .models import ChainStores, SearchResults, Baskets, SessionBasketStores, BasketSummary, Items, SessionBasketItems, SessionBasketDetails, BasketStores

SQL_SEARCH_ITEMNAME = """select * from itemname_search_results('%s', %s)"""
SQL_CITY_ARRAY = """(select array_agg(chainstoreid) from chainstores where city in ('מעלות', 'נהריה'))"""
SQL_INSERT_CITIES = """insert into basketstores(sessionid,chainstoreid) select %s, chainstoreid from chainstores a where city in ('מעלות', 'נהריה') and not exists(select basketstoreid from basketstores where sessionid=%s and chainstoreid=a.chainstoreid)"""

# Create your views here.

def get_cities():
    return ChainStores.objects.values("city").distinct().order_by("city")

def index(request):
    request.session['django_language'] = "he-il"
    context = {"cities": get_cities()}
 #   expiry = datetime.datetime.now() + datetime.timedelta(days=90)

    request.session.set_expiry(7776000)
    return render(request, "compare_prices/index.html", context)

def search(request):
    request.session['django_language'] = "he-il"
#    context = {"cities": get_cities()}
    try:
        search_term = request.POST["search_term"]
        results = SearchResults.objects.raw(SQL_SEARCH_ITEMNAME % (search_term, SQL_CITY_ARRAY))
        data = serializers.serialize("json", results)
#        context["items"] = results
        
#    except KeyError:
#        pass
    except Exception as e:
        return HttpResponse(e)
#    return render(request, "compare_prices/index.html", context)
    return HttpResponse(data, content_type='application/json')

def getsummary(request):
    results = BasketSummary.objects.filter(sessionid=request.session.session_key).order_by("-totalprice")[:3]
    data = serializers.serialize("json", results)
    return HttpResponse(data, content_type="application/json")


def addtobasket(request):
    try:
        itemcode = request.POST["itemcode"]
        qty = request.POST["qty"]
        cursor = connection.cursor()
        cursor.execute(SQL_INSERT_CITIES, [request.session.session_key, request.session.session_key])
        Baskets.objects.create(sessionid=request.session.session_key, items=Items.objects.get(itemcode=itemcode), qty=qty)
        results = BasketSummary.objects.filter(sessionid=request.session.session_key).order_by("-totalprice")[:3]
        data = serializers.serialize("json", results)
    except KeyError as e:
        return HttpResponse(0)
    return getsummary(request)

def getbasket(request):
    parms = {"sessionid":request.session.session_key}
    storeid = request.GET.get("chainstoreid", None)
    if storeid:
        parms["chainstoreid"] = storeid
    stores = serializers.serialize("json", SessionBasketStores.objects.filter(**parms))
    items = serializers.serialize("json", SessionBasketItems.objects.filter(sessionid=request.session.session_key))
    prices = serializers.serialize("json", SessionBasketDetails.objects.filter(**parms))
    totals = serializers.serialize("json", BasketSummary.objects.filter(**parms))
    results = {"stores": stores, "items": items, "prices": prices, "totals": totals}
    return HttpResponse(json.dumps(results), content_type="application/json")

def clearbasket(request):
    Baskets.objects.filter(sessionid=request.session.session_key).delete()
    BasketStores.objects.filter(sessionid=request.session.session_key).delete()
    return getsummary(request)

