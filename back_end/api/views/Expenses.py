import sys
sys.path.append("..")

from django.db.models import Sum
from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action

from phat_finance.models import Expenses
from ..serializers.expenses import ExpenseSerializer

class ExpensesPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'  # Allow client to override page size
    max_page_size = 1000

class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint to interact with Expenses model
    """
    serializer_class = ExpenseSerializer
    pagination_class = ExpensesPagination
    permission_classes = [permissions.IsAuthenticated]
    queryset = Expenses.objects.all().order_by('date')

    def get_queryset(self):
        """
        This is a manually overwriten get_queryset method \n
        Ain't nobody got time for that 🥱😴
        """
        queryset = Expenses.objects.all().order_by('date')
        date = self.request.query_params.get('date')
        user = self.request.query_params.get('user')
        category = self.request.query_params.get('category')
        if date is not None:
            queryset = queryset.filter(date=date)
        if user is not None:
            queryset = queryset.filter(user=user)
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset

    @action(detail=False, methods=['get'])
    def total(self, request):
        """
        Calculates the total expenses for the (optionally filtered) queryset.
        """
        queryset = self.get_queryset()  # Apply any filters
        total_cash = queryset.aggregate(total=Sum('cash'))['total'] or 0
        total_digital = queryset.aggregate(total=Sum('digital'))['total'] or 0
        total_credit = queryset.aggregate(total=Sum('credit'))['total'] or 0
        return Response(
                {"total_cash": total_cash,
                "total_digital":total_digital,
                "total_credit":total_credit}
                )