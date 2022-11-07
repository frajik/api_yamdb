from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from Users.models import User

from .filters import TitleFilter
from .permissions import (IsAdmin, IsAdminModeratAuthorOrReadOnly,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetJWTTokenSerializer,
                          GetTitleSerializer, MePatchSerializer,
                          NewUserRegSerializer, ReviewSerializer,
                          TitleSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"

    @action(
        methods=["get", "patch"],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        if request.method == "PATCH":
            user = get_object_or_404(User, id=request.user.id)
            serializer = MePatchSerializer(
                user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_code(request):
    if request.method == "POST":
        serializer = NewUserRegSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data["email"] = user.email
            data["username"] = user.username
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject="Confirmation code for YAMDB",
                message=f"Confirmation code: {confirmation_code}",
                from_email=None,
                recipient_list=[user.email],
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = GetJWTTokenSerializer(data=request.data)
    data = {}
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(
        User, username=serializer.validated_data["username"]
    )
    code = serializer.validated_data["confirmation_code"]
    if default_token_generator.check_token(user, code):
        token = AccessToken.for_user(user)
        data["token"] = str(token)
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"


class GenreViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.all().annotate(Avg("reviews__score")).order_by("name")
    )
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ['POST', "PATCH"]:
            return TitleSerializer
        return GetTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        IsAdminModeratAuthorOrReadOnly,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        IsAdminModeratAuthorOrReadOnly,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
