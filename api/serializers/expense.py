import sys
sys.path.append("..")

from phat_finance.models import Expense
from rest_framework import serializers

class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Expense
        fields = ['id','date', 'user', 'cash', 'digital' , 'credit', 'category', 'description']