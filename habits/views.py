from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Habit
from .serializers import HabitSerializer
from .pagination import HabitPagination
from .permissions import IsOwnerOrPublic

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrPublic]
    pagination_class = HabitPagination


    def get_queryset(self):
        queryset = Habit.objects.all()
        is_public = self.request.query_params.get('is_public', None)
        if is_public is not None:
            queryset = queryset.filter(is_public=is_public.lower() == 'true')
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PublicHabitListView(generics.ListAPIView):
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [AllowAny]