from django.contrib import admin
from StockProf_app.models import  MY_financialRatios, MY_stock, MY_stockPrice

# Register your models here.
admin.site.register(MY_financialRatios)
admin.site.register(MY_stock)
admin.site.register(MY_stockPrice)
