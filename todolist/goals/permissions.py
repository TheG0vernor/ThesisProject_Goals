from rest_framework import permissions
from rest_framework.permissions import BasePermission
from goals.models import BoardParticipant


class BoardPermission(BasePermission):
    """Определяет права доступа к доскам"""
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:  # если user не аутентифицирован, вернуть False
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj,
            ).exists()  # вернёт True, если у данной доски существует участник

        return BoardParticipant.objects.filter(
            user=request.user, board=obj,
            role=BoardParticipant.Role.owner,
        ).exists()  # вернёт True, если изменение доски производит владелец доски


class CategoryPermission(BasePermission):
    """Определяет права доступа к редактированию категорий"""
    def has_object_permission(self, request, view, obj):  # obj = категория
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj.board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]  # права доступа есть только у редактора и владельца
        ).exists()


class GoalPermission(BasePermission):
    """Определяет права доступа к CRUD целей"""
    def has_object_permission(self, request, view, obj):  # obj = цель
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.category.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj.category.board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists()


class CommentPermission(BasePermission):
    """Определяет права доступа к CRUD комментариев"""
    def has_object_permission(self, request, view, obj):  # obj = комментарий
        if request.method in permissions.SAFE_METHODS:  # безопасные методы, такие как get, разрешены
            return True
        # доступ по методу post определён в сериалайзере
        # доступ по методам put и delete определит условие:
        return obj.user == request.user
