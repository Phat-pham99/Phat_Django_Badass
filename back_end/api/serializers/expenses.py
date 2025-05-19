import sys
sys.path.append("..")

from phat_finance.models import Expenses
from rest_framework import serializers

class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Expenses
        fields = ['date', 'cash', 'digital' , 'credit', 'category', 'description']