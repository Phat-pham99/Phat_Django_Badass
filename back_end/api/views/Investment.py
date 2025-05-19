import sys
sys.path.append("..")

from django.db.models import Sum
from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action

from phat_investment.models import Investment
from ..serializers.investment import InvestmentSerializer

class InvestmentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  # Allow client to override page size
    max_page_size = 1000

class InvestmentViewSet(viewsets.ModelViewSet):
    """
    """
    serializer_class = InvestmentSerializer
    pagination_class = InvestmentPagination
    permission_classes = [permissions.IsAuthenticated]
    query = Investment.objects.all().order_by('date')

    def get_queryset(self):
        """
        """
        queryset = Investment.objects.all().order_by('date')
        date = self.request.query_params.get('date')
        investment_type = self.request.query_params.get('investment_type')
        if date is not None:
            queryset = queryset.filter(date=date)
        if investment_type  is not None:
            queryset = queryset.filter(investment_type=investment_type)
        return queryset

    @action(detail=False, methods=['GET'])
    def total(self, request):
        """
        """
        queryset = self.get_queryset()
        total_investment = queryset.aggregate(total=Sum('amount'))['total'] or 0
        return Response(
                {"Total": total_investment}
                )