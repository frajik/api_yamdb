
from django.urls import path, include
from .views import (
    TitleViewSet, GenreViewSet, CategoryViewSet,
    ReviewViewSet, CommentViewSet, UserViewSet,
    send_code, get_token
)
from rest_framework.routers import DefaultRouter


app_name = "api"
auth_patterns = [
    path("signup/", send_code, name="send_code"),
    path("token/", get_token, name="get_token"),
]

v1_router = DefaultRouter()
v1_router.register('categories', CategoryViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='title'
)
v1_router.register('genres', GenreViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
v1_router.register('titles', TitleViewSet)
v1_router.register('users', UserViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include(auth_patterns))
]
