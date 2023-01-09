from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalsFilter
from goals.models import GoalsCategory, Goals, GoalsComments, StatusGoal
from goals.serializers import GoalsCategoryCreateSerializer, GoalsCategorySerializer, GoalsCreateSerializer, \
    GoalsSerializer, GoalsCommentCreateSerializer, GoalsCommentSerializer


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


class GoalsListView(ListAPIView):
    serializer_class = GoalsSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_class = GoalsFilter

    search_fields = ['title', 'description']

    def get_queryset(self):
        return Goals.objects.filter(user=self.request.user).exclude(status=StatusGoal.archived.value[0])  # кроме тех, которые в архиве


class GoalsView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goals.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.status = Goals.status.archived[0]
        instance.save()

        return instance


class GoalCommentCreateView(CreateAPIView):
    serializer_class = GoalsCommentCreateSerializer
    permission_classes = [IsAuthenticated]


class GoalCommentListView(ListAPIView):
    serializer_class = GoalsCommentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering_fields = ['goal']
    ordering = ["-created"]  # для сортировки по убыванию

    def get_queryset(self):
        return GoalsComments.objects.filter(user=self.request.user)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalsCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GoalsComments.objects.filter(user=self.request.user)
