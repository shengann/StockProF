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
from django.http import Http404



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
        sector = request.data.get('sector')
        for Symbol in ticker_list:
            print(Symbol)
            print(sector)
            stock.objects.create( Symbol=Symbol,Sector =sector)
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
        print(((finacialRatiosSerializer(data, many=True)).data))
        data_frame = pd.DataFrame((finacialRatiosSerializer(data, many=True)).data)
        data_frame=data_frame.drop(columns=['date','id'])
        
        scaler = MinMaxScaler()
        columns = ['assetturnover', 'quickratio', 'debttoequity','roe', 'dividendyield', 'pricetoearnings']
        df_norm = pd.DataFrame(scaler.fit_transform(
            data_frame[columns]))
        df_norm.set_axis(columns, axis=1, inplace=True)
        data_frame= data_frame['ticker']
        data_frame = pd.concat([df_norm, data_frame], axis=1)
        print("data_frame\n", data_frame)
        
        lof = LocalOutlierFactor()
        lof.fit(data_frame[columns])
        lof_scores = -lof.negative_outlier_factor_
        data_frame['lof_score'] = lof_scores
        print("data_frame\n", data_frame)

        data_frame = data_frame.drop(columns=['lof_score','ticker'])
        em_clustering = BayesianGaussianMixture(n_components=3)
        print("data_frame\n", data_frame)
        em_clustering.fit(data_frame)
        labels = em_clustering.predict(data_frame)
        print("labels", labels)
        
        return (Response((finacialRatiosSerializer(data,many=True)).data))
    

class getIndustryTicker(views.APIView):
    def get(self, request, *args, **kwargs):
        sector = self.kwargs['sector']
        url = "https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=2000000000&isEtf=false&isActivelyTrading=True&sector={sector}&exchange=NASDAQ&limit=500&apikey=ae939e4358f7c5e3f91ed3594ba67d1b"
        url = url.format(sector=sector)
        response = requests.get(url)
        # sector_data = [{'symbol': 'AAPL', 'companyName': 'Apple Inc.', 'marketCap': 2321230916137, 'sector': 'Technology', 'industry': 'Consumer Electronics', 'beta': 1.277894, 'price': 146.71, 'lastAnnualDividend': 0.91, 'volume': 55344942, 'exchange': 'NASDAQ Global Select', 'exchangeShortName': 'NASDAQ', 'country': 'US', 'isEtf': False, 'isActivelyTrading': True}, {'symbol': 'MSFT', 'companyName': 'Microsoft Corporation', 'marketCap': 1855143851950, 'sector': 'Technology', 'industry': 'Software—Infrastructure', 'beta': 0.91562, 'price': 249.22, 'lastAnnualDividend': 2.54, 'volume': 24990905, 'exchange': 'NASDAQ Global Select', 'exchangeShortName': 'NASDAQ', 'country': 'US', 'isEtf': False, 'isActivelyTrading': True}, {'symbol': 'NVDA', 'companyName': 'NVIDIA Corporation', 'marketCap': 580287120000, 'sector': 'Technology', 'industry': 'Semiconductors', 'beta': 1.790446, 'price': 232.86, 'lastAnnualDividend': 0.16, 'volume': 58971591, 'exchange': 'NASDAQ Global Select', 'exchangeShortName': 'NASDAQ', 'country': 'US', 'isEtf': False, 'isActivelyTrading': True}, {'symbol': 'ASML', 'companyName': 'ASML Holding N.V.', 'marketCap': 244006574094, 'sector': 'Technology', 'industry': 'Semiconductor Equipment & Materials', 'beta': 1.232504, 'price': 618.38, 'lastAnnualDividend': 5.639, 'volume': 995900, 'exchange': 'NASDAQ Global Select', 'exchangeShortName': 'NASDAQ', 'country': 'NL', 'isEtf': False,
        #                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                'isActivelyTrading': True}, {'symbol': 'AVGO', 'companyName': 'Broadcom Inc.', 'marketCap': 240877841000, 'sector': 'Technology', 'industry': 'Semiconductors', 'beta': 1.120641, 'price': 577.75, 'lastAnnualDividend': 16.9, 'volume': 1535326, 'exchange': 'NASDAQ Global Select', 'exchangeShortName': 'NASDAQ', 'country': 'US', 'isEtf': False, 'isActivelyTrading': True}, {'symbol': 'CSCO', 'companyName': 'Cisco Systems, Inc.', 'marketCap': 198565355151, 'sector': 'Technology', 'industry': 'Communication Equipment', 'beta': 0.954672, 'price': 48.48, 'lastAnnualDividend': 1.52, 'volume': 17251578, 'exchange': 'NASDAQ Global Select', 'exchangeShortName': 'NASDAQ', 'country': 'US', 'isEtf': False, 'isActivelyTrading': True}, {'symbol': 'TXN', 'companyName': 'Texas Instruments Incorporated', 'marketCap': 153275685546, 'sector': 'Technology', 'industry': 'Semiconductors', 'beta': 1.014993, 'price': 169.14, 'lastAnnualDividend': 3.5399999999999996, 'volume': 4118305, 'exchange': 'NASDAQ Global Select', 'exchangeShortName': 'NASDAQ', 'country': 'US', 'isEtf': False, 'isActivelyTrading': True}, {'symbol': 'ADBE', 'companyName': 'Adobe Inc.', 'marketCap': 146743212000, 'sector': 'Technology', 'industry': 'Software—Infrastructure', 'beta': 1.227684, 'price': 320.54, 'lastAnnualDividend': 0, 'volume': 8444481, 'exchange': 'NASDAQ Global Select', 'exchangeShortName': 'NASDAQ', 'country': 'US', 'isEtf': False, 'isActivelyTrading': True}, {'symbol': 'QCOM', 'companyName': 'QUALCOMM Incorporated', 'marketCap': 138639107958, 'sector': 'Technology', 'industry': 'Semiconductors', 'beta': 1.291143, 'price': 124.34, 'lastAnnualDividend': 3, 'volume': 7357182, 'exchange': 'NASDAQ Global Select', 'exchangeShortName': 'NASDAQ', 'country': 'US', 'isEtf': False, 'isActivelyTrading': True}, {'symbol': 'AMD',
        #                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                'companyName': 'Advanced Micro Devices, Inc.', 'marketCap': 125909187402, 'sector': 'Technology', 'industry': 'Semiconductors', 'beta': 1.981171, 'price': 78.09, 'lastAnnualDividend': 0, 'volume': 46700007, 'exchange': 'NASDAQ Global Select', 'exchangeShortName': 'NASDAQ', 'country': 'US', 'isEtf': False, 'isActivelyTrading': True}]
        sector_data=response.json()
        symbols = [symbol['symbol'] for symbol in sector_data]
        symbols = json.dumps(symbols)
        print("sector_data", symbols)
        
        return None