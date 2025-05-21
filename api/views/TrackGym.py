import sys
sys.path.append("..")

from rest_framework import permissions, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action

from phat_fitness.models import TrackGym
from ..serializers.fitness import TrackGymSerializer

class TrackGymPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'  # Allow client to override page size
    max_page_size = 1000

class TrackGymViewSet(viewsets.ModelViewSet):
    """
    API endpoint to interact with TrackGym model
    """
    serializer_class = TrackGymSerializer
    pagination_class = TrackGymPagination
    permission_classes = [permissions.IsAuthenticated]
    queryset = TrackGym.objects.all().order_by('date')

    def get_queryset(self):
        """
        This is a manually overwriten get_queryset method \n
        Ain't nobody got time for that 🥱😴
        """
        queryset = TrackGym.objects.all().order_by('date')
        date = self.request.query_params.get('date')
        user = self.request.query_params.get('user')
        routine = self.request.query_params.get('routine')
        if date is not None:
            queryset = queryset.filter(date=date)
        if user is not None:
            queryset = queryset.filter(dauserte=user)
        if routine is not None:
            queryset = queryset.filter(routine=routine)
        return queryset

    @action(detail=False, methods=['put'])
    def change(self, request):
        """
        """
        date = self.request.data.get('date')
        user = self.request.data.get('user')
        routine = self.request.data.get('routine')
        try:
            trackgym = TrackGym.objects.get(user=user, date=date, routine=routine)
        except TrackGym.DoesNotExist:
            return Response({"error": "TrackGym not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TrackGymSerializer(trackgym, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
