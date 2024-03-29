from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from rest_framework import serializers, exceptions

from core.models import User

from django.contrib.auth import authenticate

# USER_MODEL = get_user_model() - другой вариант указания user модели


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериалайзер, обрабатывающий регистрацию пользователя"""
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

        try:  # валидатор для проверки пароля
            password_validation.validate_password(password)
        except Exception as e:
            raise serializers.ValidationError(e)

        password_hashed = make_password(password)  # только хеширует пароль, не включает проверки

        validated_data['password'] = password_hashed

        return super().create(validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """Сериалайзер, обрабатывающий аутентификацию пользователя"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        if not user:
            raise exceptions.AuthenticationFailed
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериалайзер, обрабатывающий профиль пользователя"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserChangePasswordSerializer(serializers.ModelSerializer):
    """Сериалайзер отвечает за смену пароля пользователем"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # вернёт пользователя из текущего request ниже
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['user', 'old_password', 'new_password']

    def validate(self, attrs):
        user = attrs['user']
        if not user.check_password(raw_password=attrs['old_password']):
            raise serializers.ValidationError('Incorrect password')
        return attrs

    def update(self, instance, validated_data):
        try:  # проверка пароля
            password_validation.validate_password(validated_data['new_password'])
        except Exception as e:
            raise serializers.ValidationError(e)
        instance.password = make_password(validated_data['new_password'])
        instance.save()
        return instance
