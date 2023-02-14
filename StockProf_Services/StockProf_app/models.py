from django.db import models
import datetime
from decimal import Decimal

# Create your models here.
class stock (models.Model):
    Symbol = models.CharField(max_length=50,unique=True)
    AssetType = models.CharField(max_length=20)
    Name = models.CharField(max_length=220)
    CIK = models.CharField(max_length=20, null=True, blank=True)
    Exchange = models.CharField(max_length=20)
    Currency = models.CharField(max_length=20)
    Country = models.CharField(max_length=20)
    Sector = models.CharField(max_length=20)
    Industry = models.CharField(max_length=220)
    Address = models.CharField(max_length=220,null=True, blank=True)
    
    def __str__(self):
        return self.Symbol
    
class financialRatios (models.Model):
    ticker = models.ForeignKey(
        stock, on_delete=models.CASCADE, related_name='financialRatios', to_field='Symbol', null=True, blank=True)
    # ticket = models.CharField(max_length=20)
    assetturnover = models.DecimalField(
        max_digits=6, decimal_places=4, min_value=Decimal('-9999999999.99'))
    quickratio = models.DecimalField(
        max_digits=6, decimal_places=4, min_value=Decimal('-9999999999.99'))
    debttoequity = models.DecimalField(
        max_digits=6, decimal_places=4, min_value=Decimal('-9999999999.99'))
    roe = models.DecimalField(
        max_digits=6, decimal_places=4, min_value=Decimal('-9999999999.99'))
    dividendyield = models.DecimalField(
        max_digits=6, decimal_places=4, min_value=Decimal('-9999999999.99'))
    pricetoearnings = models.DecimalField(
        max_digits=6, decimal_places=4, min_value=Decimal('-9999999999.99'))
    date = models.DateField()

    def __str__(self):
        return str(self.ticker) + "  " +str(self.date)
