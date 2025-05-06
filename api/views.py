import sys
sys.path.append("..")

from phat_finance.models.expenses import Expenses
from rest_framework import permissions, viewsets
from .serializers import ExpenseSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint to interact with Expenses model
    """
    queryset = Expenses.objects.all().order_by('date')
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]