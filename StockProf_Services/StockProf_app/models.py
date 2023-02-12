from django.db import models

# Create your models here.
class stock (models.Model):
    name = models.CharField(max_length=50)
    ticket = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
class financialRatios (models.Model):
    ticket = models.ForeignKey(stock, on_delete=models.CASCADE, related_name='financialRatios')
    assetturnover= models.IntegerField()
    quickratio = models.IntegerField()
    debttoequity = models.IntegerField()
    roe = models.IntegerField()
    dividendyield = models.IntegerField()
    pricetoearnings = models.IntegerField()
    created = models.DateField(auto_now=False, auto_now_add=False)
