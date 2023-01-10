from abc import ABC

from rest_framework import serializers

from core.serializers import UserProfileSerializer
from goals.models import GoalsCategory, Goals, GoalsComments, Board, BoardParticipant


class GoalsCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalsCategory
        read_only_fields = ["id", "created", "updated", "user", "board"]
        fields = "__all__"


class GoalsCategorySerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalsCategory
        read_only_fields = ["id", "created", "updated", "user", "board"]
        fields = "__all__"


class GoalsCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goals
        read_only_fields = ["id", "created", "updated", "user"]
        fields = "__all__"

    def validate_category(self, category: GoalsCategory):
        if category.is_deleted:
            raise serializers.ValidationError("not allowed category")
        if category.user != self.context["request"].user:
            raise serializers.ValidationError("not allowed user")
        return category


class GoalsSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Goals
        read_only_fields = ["id", "created", "updated", "user"]
        fields = "__all__"


class GoalsCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalsComments
        read_only_fields = ["id", "updated", "created", "user"]
        fields = "__all__"


class GoalsCommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalsComments
        read_only_fields = ["id", "updated", "created", "user", "goal"]
        fields = "__all__"


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ['id', 'created', 'updated']
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop['user']
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner,)
        return board


class BoardSerializer(serializers.ModelSerializer):
    pass


class BoardParticipantSerializer(serializers.ModelSerializer):
    pass
