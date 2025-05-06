import sys
sys.path.append("..")

from rest_framework import permissions, viewsets

from phat_finance.models import Expenses
from ..serializers.expenses import ExpenseSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint to interact with Expenses model
    """
    queryset = Expenses.objects.all().order_by('date')
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]