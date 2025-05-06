import sys
sys.path.append("..")

from phat_finance.models.expenses import Expenses
from rest_framework import serializers

class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Expenses
        fields = ['date', 'user', 'cash', 'digital' , 'credit', 'category']

