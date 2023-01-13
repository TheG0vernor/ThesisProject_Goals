from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalsFilter
from goals.models import GoalsCategory, Goals, GoalsComments, StatusGoal, Board
from goals.permissions import BoardPermission, CategoryPermission, GoalPermission, CommentPermission
from goals.serializers import GoalsCategoryCreateSerializer, GoalsCategorySerializer, GoalsCreateSerializer, \
    GoalsSerializer, GoalsCommentCreateSerializer, GoalsCommentSerializer, BoardListSerializer, BoardSerializer, \
    BoardCreateSerializer


class GoalsCategoryCreateView(CreateAPIView):
    queryset = GoalsCategory.objects.all()  # если модель определена в сериализаторе, model или queryset можно не указывать
    serializer_class = GoalsCategoryCreateSerializer
    permission_classes = [IsAuthenticated, CategoryPermission]


class GoalsCategoryListView(ListAPIView):
    queryset = GoalsCategory.objects.all()
    serializer_class = GoalsCategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self):
        return GoalsCategory.objects.filter(board__participants__user=self.request.user,
                                            is_deleted=False)


class GoalsCategoryView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalsCategorySerializer
    permission_classes = [IsAuthenticated, CategoryPermission]

    def get_queryset(self):
        return GoalsCategory.objects.filter(board__participants__user=self.request.user,
                                            is_deleted=False)

    def perform_destroy(self, instance):  # переопределение метода destroy
        instance.is_deleted = True
        instance.save()
        return instance


class GoalsCreateView(CreateAPIView):
    serializer_class = GoalsCreateSerializer
    permission_classes = [IsAuthenticated, GoalPermission]


class GoalsListView(ListAPIView):
    serializer_class = GoalsSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = GoalsFilter
    ordering_fields = ['-priority', 'due_date']
    ordering = ['-priority', '-due_date']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Goals.objects.filter(category__board__participants__user=self.request.user).exclude(status=StatusGoal.archived)  # кроме тех, которые в архиве


class GoalsView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalsSerializer
    permission_classes = [IsAuthenticated, GoalPermission]

    def get_queryset(self):
        return Goals.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.status = Goals.status.archived[0]
        instance.save()

        return instance


class GoalCommentCreateView(CreateAPIView):
    serializer_class = GoalsCommentCreateSerializer
    permission_classes = [IsAuthenticated, CommentPermission]


class GoalCommentListView(ListAPIView):
    serializer_class = GoalsCommentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ['created']
    ordering = ["-created"]  # для сортировки по убыванию
    filterset_fields = ['goal']

    def get_queryset(self):
        return GoalsComments.objects.filter(goal__category__board__participants__user=self.request.user)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalsCommentSerializer
    permission_classes = [IsAuthenticated, CommentPermission]

    def get_queryset(self):
        return GoalsComments.objects.filter(goal__category__board__participants__user=self.request.user)


class BoardCreateView(CreateAPIView):
    serializer_class = BoardCreateSerializer
    permission_classes = [IsAuthenticated, BoardPermission]


class BoardListView(ListAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [IsAuthenticated, BoardPermission]

    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering_fields = ['title']
    ordering = ["title"]

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardView(RetrieveUpdateDestroyAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, BoardPermission]

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goals.objects.filter(category__board=instance).update(
                status=StatusGoal.archived.value[0])
            return instance
