from rest_framework import serializers
from accInfo.models import savedResult


class savedResultSerializer(serializers.ModelSerializer):
    clusteredStocksSymbols = serializers.ListField(
        child=serializers.ListField(child=serializers.CharField()))

    outlierStocksSymbols = serializers.ListField()
    portfolioTypeOptions = serializers.ListField()


    class Meta:
        model = savedResult
        fields = ['id', 'user', 'clusteredStocksSymbols','outlierStocksSymbols', 'portfolioTypeOptions']
