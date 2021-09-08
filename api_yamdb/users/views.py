from django.core.mail import send_mail
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import RegisterUserSerializer
from .models import User


class CreateUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            new_user = get_object_or_404(User, email=request.data['email'])
            confirmation_code = str(RefreshToken.for_user(new_user))
            send_mail(
                'Код подтверждения',
                f'Ваш код: {confirmation_code}',
                'from@example.com',
                [f'{new_user.email}'],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
