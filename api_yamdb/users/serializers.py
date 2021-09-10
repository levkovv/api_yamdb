from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, args):
        email = args.get('email', None)
        username = args.get('username', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Такая электронная почта уже существует')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Такое имя пользователя уже существует')
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.')
        return super().validate(args)

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class TokenRefreshSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    token = serializers.ReadOnlyField()

    def validate(self, attrs):
        data = super().validate(attrs)
        username = attrs.get('username', None)
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Такое пользователя не существует')
        refresh = RefreshToken(attrs['confirmation_code'])
        data = {'token': str(refresh.access_token)}
        data['confirmation_code'] = str(refresh)
        return data
