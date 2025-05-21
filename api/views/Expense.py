import sys
sys.path.append("..")

from django.db.models import Sum
from rest_framework import permissions, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action

from phat_finance.models import Expense
from ..serializers.expense import ExpenseSerializer

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
    queryset = Expense.objects.all().order_by('date')

    def get_queryset(self):
        """
        This is a manually overwriten get_queryset method \n
        Ain't nobody got time for that 🥱😴
        """
        queryset = Expense.objects.all().order_by('date')
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

    @action(detail=False, methods=['put'])
    def change(self, request):
        """
        Update an existing expense item.
        """
        date = self.request.data.get('date')
        user = self.request.data.get('user')
        category = self.request.data.get('category')
        try:
            expense = Expense.objects.get(date=date, user=user, category=category)
            print("expense", expense)
        except Expense.DoesNotExist:
            print({"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)
            return Response({"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExpenseSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def delete(self, request):
        """
        Delete an existing expense item.
        """
        date = self.request.data.get('date')
        user = self.request.data.get('user')
        category = self.request.data.get('category')
        try:
            expense = Expense.objects.get(date=date, user=user, category=category)
        except Expense.DoesNotExist:
            return Response({"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
