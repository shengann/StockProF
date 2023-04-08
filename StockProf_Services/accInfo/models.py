from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models
from StockProf_app.models import  MY_financialRatios

class savedResult(models.Model):
    user = models.ForeignKey(User, related_name='savedResult', on_delete=models.CASCADE)
    clusteredStocksSymbols = models.JSONField(default=list)
    outlierStocksSymbols = models.JSONField(default=list)
    portfolioTypeOptions = models.JSONField(default=list)
    stockTypeOptions = models.JSONField(default=list)
    category = models.CharField(max_length=220, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=220, blank=True)
    
    def __str__(self):
        return f"{self.user}\t{self.category}\t{self.date_created}"
