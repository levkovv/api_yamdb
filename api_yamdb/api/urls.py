from django.urls import path

from users.views import CreateUser, TokenObtain


urlpatterns = [
    path('v1/auth/signup/', CreateUser.as_view(), name='create_user'),
    path('v1/auth/token/', TokenObtain.as_view(), name='get_token'),
]
