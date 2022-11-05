from django.urls import path, include
from .views import (
    TitleViewSet, GenreViewSet, CategoryViewSet,
    ReviewViewSet, CommentViewSet, UserViewSet,
    send_code, get_token
)
from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register('users', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename="reviews"
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename="comments"
)

urlpatterns = [
    path("v1/auth/signup/", send_code, name="send_code"),
    path("v1/auth/token/", get_token, name="get_token"),
    path('v1/', include(router.urls)),
]
