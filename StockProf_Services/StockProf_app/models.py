from django.db import models
import datetime

# Create your models here.
class stock (models.Model):
    Symbol = models.CharField(max_length=50,unique=True)
    AssetType = models.CharField(max_length=20,blank=True)
    Name = models.CharField(max_length=220, blank=True)
    CIK = models.CharField(max_length=20, null=True, blank=True)
    Exchange = models.CharField(max_length=20, blank=True)
    Currency = models.CharField(max_length=20, blank=True)
    Country = models.CharField(max_length=20, blank=True)
    Sector = models.CharField(max_length=20)
    Industry = models.CharField(max_length=220, blank=True)
    Address = models.CharField(max_length=220,null=True, blank=True)
    
    def __str__(self):
        return str(self.Symbol) + "  " + str(self.Name)
    
class financialRatios (models.Model):
    ticker = models.ForeignKey(
        stock, on_delete=models.CASCADE, related_name='financialRatios', to_field='Symbol', null=True, blank=True)
    # ticket = models.CharField(max_length=20)
    assetturnover = models.DecimalField(max_digits=10, decimal_places=4)
    quickratio = models.DecimalField(max_digits=10, decimal_places=4)
    debttoequity = models.DecimalField(max_digits=10, decimal_places=4)
    roe = models.DecimalField(max_digits=10, decimal_places=4)
    dividendyield = models.DecimalField(max_digits=10, decimal_places=4)
    pricetoearnings = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateField()

    def __str__(self):
        return str(self.ticker) + "  " +str(self.date)
