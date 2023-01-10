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
