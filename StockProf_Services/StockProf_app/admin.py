from django.contrib import admin
from StockProf_app.models import stock, financialRatios, MY_financialRatios, MY_stock

# Register your models here.
admin.site.register(stock)
admin.site.register(financialRatios)
admin.site.register(MY_financialRatios)
admin.site.register(MY_stock)
