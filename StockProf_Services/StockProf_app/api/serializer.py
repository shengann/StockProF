from rest_framework import serializers
from StockProf_app.models import MY_financialRatios, MY_stock, MY_stockPrice

class MY_finacialRatiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MY_financialRatios
        fields = '__all__'


class MY_stockSerializer(serializers.ModelSerializer):
    financial_ratios = MY_finacialRatiosSerializer(many=True, read_only=True)
    class Meta:
        model = MY_stock
        fields = (
            "id",
            "Symbol",
            "Name",
            "get_absolute_url",
            "Category",
            'financial_ratios'
        )


class MY_stockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MY_stockPrice
        fields = '__all__'
