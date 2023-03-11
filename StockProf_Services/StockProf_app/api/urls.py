from django.urls import path, include
from rest_framework.routers import DefaultRouter
from StockProf_app.api.views import getStockData, getFinancialRatosData, getStockProfData, getIndustryTicker

router = DefaultRouter()
urlpatterns = [
    path('stock', getStockData.as_view(), name='get-Stock-Data'),
    path('stock/financial_ratio',
         getFinancialRatosData.as_view(), name='getFinancialRatosData'),
    path('LOF', getStockProfData.as_view(), name='getStockProfData'),
    path('industry/<str:sector>', getIndustryTicker.as_view(),
         name='getIndustryTicker')

]
