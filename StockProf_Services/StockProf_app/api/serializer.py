from rest_framework import serializers
from StockProf_app.models import stock, financialRatios, MY_financialRatios, MY_stock

class finacialRatiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = financialRatios
        # dataDate = serializers.DateTimeField(format="%Y-%m-%d")
        fields = '__all__'
        
        
class stockSerializer(serializers.ModelSerializer):
    # financialRatios = finacialRatiosSerializer(many=True)
    class Meta:
        model = stock
        fields = (
            "id",
            "Symbol",
            "Name",
            "get_absolute_url",
            "Exchange",
            "Sector",
            "Industry",
        )
        

class finacial_ratiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MY_financialRatios
        fields = '__all__'


class StocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = MY_stock
        fields = (
            "id",
            "Symbol",
            "Name",
            "get_absolute_url",
            "Exchange",
            "Sector",
            "Industry",
        )
