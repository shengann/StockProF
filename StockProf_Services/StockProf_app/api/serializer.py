from rest_framework import serializers
from StockProf_app.models import stock, financialRatios

class finacialRatiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = financialRatios
        # dataDate = serializers.DateTimeField(format="%Y-%m-%d")
        fields = '__all__'
        
        
class stockSerializer(serializers.ModelSerializer):
    # financialRatios = finacialRatiosSerializer(many=True)
    class Meta:
        model = stock
        fields = '__all__'
        
