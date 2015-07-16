from django.shortcuts import render
from django.http import HttpResponse

from .models import SearchResults

SQL_SEARCH_ITEMNAME = """select * from itemname_search_results('%s', '%s')"""

# Create your views here.

def index(request):
    request.session['django_language'] = "he-il"
    return HttpResponse("This is a Hello World Test")

def search(request, search_term=None):
    request.session['django_language'] = "he-il"

html = """<table border=1><tr><th>Item Code</th><th>Item Name</th><th>Qty</th><th>Unit Qty</th><th>Min Price</th><th>Max Price</th><th>Details</th></tr>"""
    for row in SearchResults.objects.raw(
            SQL_SEARCH_ITEMNAME % (search_term,
                "{339, 397, 406, 489, 1775, 1782, 1910}")):
        html += """<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" %(row.itemcode, row.itemname, row.quantity, row.unitqty, row.minprice, row.maxprice, row.details)
    html += "</table>"
    return HttpResponse(html)

