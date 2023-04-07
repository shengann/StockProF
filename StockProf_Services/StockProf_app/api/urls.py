from django.urls import path, include
from rest_framework.routers import DefaultRouter
from StockProf_app.api.views import getStockPriceData, getStockProfData, stockList, filterStock, MY_getFinancialRatiosData, MY_getStockPrice, MY_getComparison, filterFinancialRatio, getBoxPlotData, getPastPortfolioData

router = DefaultRouter()
router.register("stocks",stockList,basename="stocks")
urlpatterns = [
    path('',include(router.urls)),
    path('stocks/<str:Category>', filterStock.as_view(), name='filterStock'),
    path('stocks/<str:Category>/financial-ratio', filterFinancialRatio.as_view(),name='filterFinancialRatio'),
    path('stock/<slug:ticker>', getStockPriceData.as_view(), name='get-Stock-Data'),
    path('stockprof', getStockProfData.as_view(), name='getStockProfData'),
    path('financial-ratio', MY_getFinancialRatiosData.as_view(),name='MY_getFinancialRatiosData'),
    path('stock-price', MY_getStockPrice.as_view(), name='stock-price'),
    path('comparison', MY_getComparison.as_view(), name='comparison'),
    path('portfolio/box-plot-data', getBoxPlotData.as_view()),
    path('user-portfolio-details', getPastPortfolioData.as_view())
]
