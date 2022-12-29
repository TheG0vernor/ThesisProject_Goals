
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from goals.models import GoalsCategory
from goals.serializers import GoalsCreateSerializer


class GoalsCategoryCreateView(CreateAPIView):
    queryset = GoalsCategory.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GoalsCreateSerializer
