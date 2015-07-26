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

    class Meta:
        db_table = "chainstores"


class Items(models.Model):
    itemcode = models.TextField(primary_key=True, db_column="itemcode")
    itemname = models.TextField()
    manufacturername = models.TextField()
    bisweighted = models.BooleanField()
    unitqty = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "items"

class Baskets(models.Model):
    basketid = models.AutoField(primary_key=True)
    sessionid = models.TextField()
    items = models.ForeignKey('Items', db_column="itemcode")

    class Meta:
        db_table = "baskets"

class BasketStores(models.Model):
    basketstoreid = models.AutoField(primary_key=True)
    sessionid = models.TextField()
    chainstoreid = models.IntegerField()

    class Meta:
        db_table = "basketstores"

class BasketSummary(models.Model):
    chainstoreid = models.IntegerField(primary_key=True)
    chainname = models.TextField()
    storename = models.TextField()
    city = models.TextField()
    sessionid = models.TextField()
    numitems = models.IntegerField()
    totalprice = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "basketsummary"


class SessionBasketStores(models.Model):
    chainstoreid = models.IntegerField(primary_key=True)
    chainname = models.TextField()
    storename = models.TextField()
    city = models.TextField()
    sessionid = models.TextField()

    class Meta:
        db_table = "sessionbasketstores"


class SessionBasketItems(models.Model):
    basketid = models.IntegerField(primary_key=True)
    sessionid = models.TextField()
    itemcode = models.TextField()
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    itemname = models.TextField()

    class Meta:
        db_table = "sessionbasketitems"

class SessionBasketDetails(models.Model):
    id = models.TextField(primary_key=True),
    chainstoreid = models.IntegerField(),
    itemcode = models.TextField()
    itemprice = models.DecimalField(max_digits=10, decimal_places=2)
    sessionid = models.TextField()

    class Meta:
        db_table = "sessionbasketdetails"
 
