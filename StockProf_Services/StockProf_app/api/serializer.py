from rest_framework import serializers
from StockProf_app.models import MY_financialRatios, MY_stock, MY_stockPrice

class MY_finacial_ratiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MY_financialRatios
        fields = '__all__'


class MY_stockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MY_stock
        fields = (
            "id",
            "Symbol",
            "Name",
            "get_absolute_url",
            "Category"
        )


class MY_stockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MY_stockPrice
        fields = '__all__'
