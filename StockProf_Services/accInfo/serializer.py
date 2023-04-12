from rest_framework import serializers
from accInfo.models import savedResult


class savedResultSerializer(serializers.ModelSerializer):
    clusteredStocksSymbols = serializers.ListField(
        child=serializers.ListField(child=serializers.CharField()))

    outlierStocksSymbols = serializers.ListField()
    portfolioTypeOptions = serializers.ListField()
    stockTypeOptions = serializers.ListField()


    class Meta:
        model = savedResult
        fields = ['id', 'user', 'category', 'clusteredStocksSymbols','outlierStocksSymbols', 'portfolioTypeOptions', 'stockTypeOptions','remarks']
        

class MyHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = savedResult
        fields = (
            "id",
            "clusteredStocksSymbols",
            "outlierStocksSymbols", 
            "portfolioTypeOptions",
            "stockTypeOptions",
            "category",
            "date_created",
            "remarks"
        )
