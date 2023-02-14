import requests
import json
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from StockProf_app.models import financialRatios, stock
from StockProf_app.api.serializer import finacialRatiosSerializer, stockSerializer
from rest_framework import views
import pandas as pd
from datetime import datetime as dt
# from django_pandas.io import read_frame, to_model

class getFinancialRatosData(views.APIView):
    queryset = financialRatios.objects.all()
    serializer_class = finacialRatiosSerializer

    def get(self, request, *args, **kwargs):
        Symbol = self.kwargs['Symbol']
        print(Symbol)
        stockList = []
        tag = ['assetturnover', 'quickratio', 'debttoequity', 'roe', 'pricetoearnings', 'dividendyield']
        ticker = Symbol
        for x in tag:
            url = "https://www.discoverci.com/charts/anychart_data?tag={tag}&ticker={ticker}&type=QTR"
            print(ticker,'ticker')
            tag = x
            url = url.format(tag=tag, ticker=ticker)
            print("url",url)
            response = requests.get(url)
            data = response.json()

            # Create a Pandas DataFrame from the data
            x = pd.DataFrame(data, columns=['date', x])
            x["date"] = pd.DatetimeIndex(x["date"])
            x["date"] = x["date"].dt.strftime('%Y-%m')

            # Set the date column as the index of the DataFrame
            # x.set_index("date", inplace=True)
            stockList.append(x)
        df_outer = stockList[0].merge(stockList[1], on='date', how='outer').merge(stockList[2], on='date', how='outer').merge(stockList[3], on='date', how='outer').merge(stockList[4], on='date', how='outer').merge(stockList[5], on='date', how='outer')
        df_outer['ticker'] = ticker
        df_outer['date'] = pd.to_datetime(df_outer['date'] + '-01')
        df_outer['date'] = df_outer['date'].dt.strftime('%Y-%m-%d')
        df_outer = df_outer.dropna()
        print("df_outer_1", df_outer)
        for i, row in df_outer.iterrows():
            stockTicker = stock.objects.get(Symbol=ticker)
            financialRatios.objects.create(ticker=stockTicker,date=row['date'], assetturnover=row['assetturnover'], quickratio=row['quickratio'], roe=row['roe'], pricetoearnings=row['pricetoearnings'], dividendyield=row['dividendyield'], debttoequity=row['debttoequity'])
        return Response((stockSerializer(stock.objects.get(Symbol=Symbol))).data)

    def post(self, request, *args, **kwargs):
        serializer = stockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class getStockData(views.APIView):
    queryset = stock.objects.all()
    serializer_class = stockSerializer
    
    def get(self, request, *args, **kwargs):
        Symbol = self.kwargs['Symbol']
        url = "https://www.alphavantage.co/query?function=OVERVIEW&symbol={Symbol}&apikey=L208XLE1W0W61EMK"
       
        url =url.format(Symbol=Symbol)
        response = requests.get(url)
        stock_data = response.json()
        serializer = stockSerializer(data=stock_data)
        if serializer.is_valid():
            serializer.save()
            return Response((stockSerializer(stock.objects.get(Symbol=Symbol))).data)

    def post(self, request, *args, **kwargs):
        serializer = stockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        
