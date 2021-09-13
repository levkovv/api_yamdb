from django.core.mail import send_mail
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdminPermission
from .serializers import (RegisterUserSerializer, TokenRefreshSerializer,
                          UserSerializer)


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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtain(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data['username']
        if User.objects.filter(username=username):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TokenRefreshSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminAPiViews(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminPermission]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)


class ReceivingChangingMyself(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user
