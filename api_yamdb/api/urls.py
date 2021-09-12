from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import (
    CreateUser, TokenObtain,
    AdminAPiViews, ReceivingChangingMyself)
from .views import (
    TitleViewSet, CategoryViewSet,
    GenreViewSet, ReviewViewSet,
    CommentViewSet
)

router = DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'users', AdminAPiViews)
router.register(r'users/me', ReceivingChangingMyself, basename='myself')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', CreateUser.as_view(), name='create_user'),
    path('v1/auth/token/', TokenObtain.as_view(), name='get_token'),
]
