from abc import ABC

from rest_framework import serializers

from core.serializers import UserProfileSerializer
from goals.models import GoalsCategory


class GoalsCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalsCategory
        read_only_fields = ["id", "created", "updated", "user"]
        fields = '__all__'


class GoalsCategorySerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalsCategory
        read_only_fields = ['id', 'created', 'updated', 'user']
        fields = '__all__'
