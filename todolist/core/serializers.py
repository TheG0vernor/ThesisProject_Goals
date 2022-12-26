from django.contrib.auth import password_validation
from rest_framework import serializers

from core.models import User

# USER_MODEL = get_user_model() - другой вариант указания user модели


class UserRegisterSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    password = serializers.CharField(write_only=True)  # атрибут ничего не возвращает на frontend, только принимает эти поля
    password_repeat = serializers.CharField(write_only=True)  # password и password_repeat придут с fronta

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.get('password')
        password_repeat = validated_data.pop('password_repeat')  # достанет значение из validated_data по ключу и удалит его из v_d

        if password != password_repeat:
            raise serializers.ValidationError('Re-entry password')

        # try:
        #     password_validation.validate_password(password)
        # except Exception as e:
        #     raise serializers.ValidationError(e)

        from django.contrib.auth.hashers import make_password
        password_hashed = make_password(password)  # не только хеширует пароль, но и включает валидаторы на проверку пароля. Если не сработает, разблокировать валидатор в try

        validated_data['password'] = password_hashed

        return super().create(validated_data)
