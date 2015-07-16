from django.db import models

# Create your models here.

class SearchResults(models.Model):
    itemcode = models.TextField(primary_key=True)
    itemname = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unitqty = models.TextField()
    minprice = models.DecimalField(max_digits=10, decimal_places=2)
    maxprice = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()

class ChainStores(models.Model):
    chainstoreid = models.IntegerField(primary_key=True)
    storename = models.TextField()
    address = models.TextField()
    city = models.TextField()
