from abc import ABC

from django.db import transaction
from rest_framework import serializers

from core.models import User
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
        user = validated_data.pop('user')
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner,)
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all(),
    )
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.Role
    )

    class Meta:
        model = BoardParticipant
        read_only_fields = ['id', 'created', 'updated', 'board']
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ["id", "created", "updated"]
        fields = '__all__'

    def update(self, instance, validated_data):
        owner = validated_data.pop('user')
        new_participants = validated_data.pop('participants')
        new_by_id = {part['user'].id: part for part in new_participants}

        other_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for other_participant in other_participants:
                if other_participant.user_id not in new_by_id:
                    other_participant.delete()
                else:
                    if other_participant.role != new_by_id[other_participant.user_id]['role']:
                        other_participant.role = new_by_id[other_participant.user_id]['role']
                        other_participant.save()
                    new_by_id.pop(other_participant.user_id)
            for new_participant in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_participant['user'],
                    role=new_participant['role'],
                )
            instance.title = validated_data['title']
            instance.save()


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
