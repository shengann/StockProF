from django.db import models

# Create your models here.
class MY_stock (models.Model):
    Symbol = models.CharField(max_length=50,unique=True)
    Name = models.CharField(max_length=220, blank=True)
    Category = models.CharField(max_length=220, blank=True)
    
    def __str__(self):
        return str(self.Symbol) + "  " + str(self.Name)
    
    def get_absolute_url(self):
        return f'/{self.Symbol}'
    
class MY_financialRatios (models.Model):
    ticker = models.ForeignKey(MY_stock, on_delete=models.CASCADE, related_name='financial_ratios', to_field='Symbol', null=True, blank=True)
    assetturnover = models.DecimalField(max_digits=10, decimal_places=4)
    quickratio = models.DecimalField(max_digits=10, decimal_places=4)
    debttoequity = models.DecimalField(max_digits=10, decimal_places=4)
    roe = models.DecimalField(max_digits=10, decimal_places=4)
    dividendyield = models.DecimalField(max_digits=10, decimal_places=4)
    pricetoearnings = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return str(self.ticker) 
    

class MY_stockPrice (models.Model):
    ticker = models.ForeignKey(MY_stock, on_delete=models.CASCADE,related_name='stock_price', to_field='Symbol', null=True, blank=True)
    open = models.DecimalField(max_digits=15, decimal_places=4)
    high = models.DecimalField(max_digits=15, decimal_places=4)
    low = models.DecimalField(max_digits=15, decimal_places=4)
    close = models.DecimalField(max_digits=15, decimal_places=4)
    volume = models.DecimalField(max_digits=15, decimal_places=4)
    date = models.DateField()


    def __str__(self):
        return str(self.ticker) + "  " + str(self.date)
