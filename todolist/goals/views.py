from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from goals.models import GoalsCategory
from goals.serializers import GoalsCategoryCreateSerializer, GoalsCategorySerializer, GoalsCreateSerializer


class GoalsCategoryCreateView(CreateAPIView):
    queryset = GoalsCategory.objects.all()  # если модель определена в сериализаторе, model или queryset можно не указывать
    serializer_class = GoalsCategoryCreateSerializer
    permission_classes = [IsAuthenticated]


class GoalsListCategoryView(ListAPIView):
    queryset = GoalsCategory.objects.all()
    serializer_class = GoalsCategorySerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self):
        return GoalsCategory.objects.filter(user=self.request.user, is_deleted=False)


class GoalsCategoryView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalsCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GoalsCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):  # переопределение метода destroy
        instance.is_deleted = True
        instance.save()
        return instance


class GoalsCreateView(CreateAPIView):
    serializer_class = GoalsCreateSerializer
    permission_classes = [IsAuthenticated]


