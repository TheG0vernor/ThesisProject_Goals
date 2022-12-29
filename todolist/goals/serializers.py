from rest_framework import serializers

from goals.models import GoalsCategory


class GoalsCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalsCategory
        read_only_fields = ["id", "created", "updated", "user"]
        fields = '__all__'
