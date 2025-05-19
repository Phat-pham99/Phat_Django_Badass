import sys
sys.path.append("..")

from phat_investment.models import Investment
from rest_framework import serializers

class InvestmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Investment
        fields = ['date','investment_type','amount']