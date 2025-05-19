import sys
sys.path.append("..")

from rest_framework import permissions, viewsets

from phat_investment.models.track_investment import TrackInvestment
from ..serializers.track_investment import TrackInvestmentSerializer

class TrackInvestmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint to interact with TrackInvestment model
    """
    queryset = TrackInvestment.objects.all().order_by('date')
    serializer_class = TrackInvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]