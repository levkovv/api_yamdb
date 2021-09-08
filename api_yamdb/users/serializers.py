from rest_framework import serializers

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
