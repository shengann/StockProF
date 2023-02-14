from django.urls import path, include
from rest_framework.routers import DefaultRouter
from StockProf_app.api.views import  getStockData, getFinancialRatosData

router = DefaultRouter()
urlpatterns = [
    path('stock/<str:Symbol>', getStockData.as_view(), name='get-Stock-Data'),
    path('stock/<str:Symbol>/financial_ratio',
         getFinancialRatosData.as_view(), name='getFinancialRatosData'),

]
