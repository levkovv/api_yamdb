from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import CreateUser


urlpatterns = [
    path('v1/auth/signup/', CreateUser.as_view(), name='create_user'),
    path('v1/auth/token/', TokenRefreshView.as_view(), name='get_token'),
]
