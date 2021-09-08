from users.views import CreateUser, TokenObtain
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CreateUser
from .views import TitleViewSet, CategoryViewSet, GenreViewSet


router = DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', CreateUser.as_view(), name='create_user'),
    path('v1/auth/token/', TokenObtain.as_view(), name='get_token'),
]
