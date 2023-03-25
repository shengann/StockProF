import requests
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from StockProf_app.models import financialRatios, stock
from StockProf_app.api.serializer import finacialRatiosSerializer, stockSerializer
from rest_framework import views
import pandas as pd
from datetime import datetime as dt
from django.utils import timezone
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import LocalOutlierFactor
from sklearn.mixture import BayesianGaussianMixture
from django.http import HttpResponse, HttpResponseNotFound


class filterStock(APIView):
    def get(self, request, *args, **kwargs):
        sector = self.kwargs['sector']
        stocks = stock.objects.filter(Sector=sector)
        serializer = stockSerializer(stocks, many=True)
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        sector = self.kwargs['sector']
        stocks = stock.objects.filter(Sector=sector)
        stocks.delete()
        return None

    
class stockList(APIView):
    def get(self, request, format=None):
        stocks = stock.objects.all()
        serializer = stockSerializer(stocks, many=True)
        return Response(serializer.data)
    
class getFinancialRatosData(views.APIView):
    def post(self, request, *args, **kwargs):
        ticker_list = request.data.get('ticker_list')
        for Symbol in ticker_list:
            print(Symbol)
            stockList = []
            tags = ['assetturnover', 'quickratio', 'debttoequity','roe', 'pricetoearnings', 'dividendyield']
            ticker = Symbol
            
            for x in tags:
                url = "https://www.discoverci.com/charts/anychart_data?tag={tag}&ticker={ticker}&type=QTR"
                tag = x
                url = url.format(tag=tag, ticker=ticker)
                
                response = requests.get(url)
                data = response.json()
                
                x = pd.DataFrame(data, columns=['date', x])
                x["date"] = pd.DatetimeIndex(x["date"])
                x['date'] = pd.PeriodIndex(x.date, freq='Q')
                stockList.append(x)
                
            df_outer = stockList[0].merge(stockList[1], on='date', how='outer').merge(stockList[2], on='date', how='outer').merge(stockList[3], on='date', how='outer').merge(stockList[4], on='date', how='outer').merge(stockList[5], on='date', how='outer')
            df_outer['ticker'] = ticker
            df_outer.drop(df_outer[df_outer["date"] <'2018Q1'].index, inplace=True)
            df_outer['date'] = df_outer['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

            df_outer[['pricetoearnings']] = df_outer[['pricetoearnings']].fillna(value=0)
            df_outer = df_outer.dropna()
            print("df_outer_1", df_outer)
            
            for i, row in df_outer.iterrows():
                stockTicker = stock.objects.get(Symbol=ticker)
                financialRatios.objects.create(ticker=stockTicker, date=row['date'], assetturnover=row['assetturnover'], quickratio=row['quickratio'],
                                            roe=row['roe'], pricetoearnings=row['pricetoearnings'], dividendyield=row['dividendyield'], debttoequity=row['debttoequity'])
        return None


class getStockData(views.APIView):
    
    def get(self, request, *args, **kwargs):
        ticker = self.kwargs['ticker']
        stock_object = stock.objects.filter(Symbol=ticker)
        print("stock_object", stock_object)
        fianacial_ratio = financialRatios.objects.filter(ticker__in=stock_object)
        serializer = finacialRatiosSerializer(fianacial_ratio, many=True)
        return Response(serializer.data)
        
    def post(self, request, *args, **kwargs):
        ticker_list = request.data.get('ticker_list')
        name_list = request.data.get('name_list')
        industry_list = request.data.get('industry_list')
        sector = request.data.get('sector')
        for Symbol, Name, Industry in zip(ticker_list, name_list, industry_list):
            print(Symbol)
            print(sector)
            stock.objects.create(Symbol=Symbol, Sector=sector,
                                 Name=Name, Industry=Industry)
        return None
        

# test data for getStockProfData
# {
#     "ticker_list": ["AAPL", "IBM", "MSFT", "V", "INTC", "PYPL"],
#     "date": "2021-12-01"
# }
class getStockProfData(views.APIView):   
    def post(self, request, format=None):
        ticker_list = request.data.get('ticker_list')
        date_data = request.data.get('date')

        stockTicker = stock.objects.filter(Symbol__in=ticker_list)
        date = timezone.datetime.strptime(date_data, '%Y-%m-%d').date()
        data = financialRatios.objects.filter(ticker__in=stockTicker, date__exact=date)
        
        data_frame = pd.DataFrame((finacialRatiosSerializer(data, many=True)).data)
        pd.set_option('display.max_rows', None)
        print("data_frame\n", data_frame)
        data_frame=data_frame.drop(columns=['date','id'])
        
        scaler = MinMaxScaler()
        columns = ['assetturnover', 'quickratio', 'debttoequity','roe', 'dividendyield', 'pricetoearnings']
        df_norm = pd.DataFrame(scaler.fit_transform(data_frame[columns]))
        df_norm.set_axis(columns, axis=1, inplace=True)
        data_frame= data_frame['ticker']
        data_frame = pd.concat([df_norm, data_frame], axis=1)
        pd.set_option('display.max_rows', None)
        print("data_frame\n", data_frame)
        
        lof = LocalOutlierFactor()
        lof.fit(data_frame[columns])
        lof_scores = -lof.negative_outlier_factor_
        data_frame['lof_score'] = lof_scores
        data_frame.drop(data_frame[data_frame["lof_score"] > 1.5].index, inplace=True)
        data_frame = data_frame.reset_index(drop=True)
        pd.set_option('display.max_rows', None)
        print("data_frame_lof\n", data_frame)

        data_frame_clustering = data_frame.drop(columns=['lof_score','ticker'])
        em_clustering = BayesianGaussianMixture(n_components=3)
        em_clustering.fit(data_frame_clustering)
        labels = em_clustering.predict(data_frame_clustering)
        print("labels", labels)
        data_frame['label'] = labels
        data_frame = data_frame.drop(columns=['assetturnover', 'quickratio', 'debttoequity', 'roe', 'dividendyield', 'pricetoearnings', 'lof_score'])
        pd.set_option('display.max_rows', None)
        print("data_frame_clustering\n", data_frame)
        
        groups = data_frame.groupby('label')
        lists = []


        for name, group in groups:
            lists.append(group['ticker'].tolist())

        # Print the list of lists
        print(lists)
        clusteringList=[]
        for ticker_list in lists:
            print("\n",ticker_list)
            clusteredStocks = stock.objects.filter(Symbol__in=ticker_list) 
            serializer = stockSerializer(clusteredStocks, many=True)
            clusteringList.append(serializer.data)
        
        print("clusteringList", clusteringList)
        content = {
            'status': 1,
            'data': clusteringList,

        }
        return Response(content)
    

class getIndustryTicker(views.APIView):
    def get(self, request, *args, **kwargs):
        sector = self.kwargs['sector']
        url = "https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=2000000000&isEtf=false&isActivelyTrading=True&sector={sector}&exchange=NASDAQ&limit=500&apikey=ae939e4358f7c5e3f91ed3594ba67d1b"
        url = url.format(sector=sector)
        response = requests.get(url)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
        sector_data=response.json()
        symbolList = []
        NameList = []
        industryList = []
        for obj in sector_data:
            symbolList.append(obj['symbol'])
            NameList.append(obj['companyName'])
            industryList.append(obj['industry'])
        symbolList = json.dumps(symbolList)
        NameList = json.dumps(NameList)
        industryList = json.dumps(industryList)
        print(symbolList, "\n")
        print(NameList, "\n")
        print(industryList, "\n")
        
        return None