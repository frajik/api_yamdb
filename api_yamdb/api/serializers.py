import datetime as dt


from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title
from Users.models import ROLE_CHOICES, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields=("username", "email", "first_name", "last_name", "bio", "role")
        model=User

    def validate_username(self, username):
        duplicate_name = User.objects.filter(
            username=username
        ).exists()
        if username == "me":
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено."
            )
        if duplicate_name:
            raise serializers.ValidationError(
                f"Пользователь с именем '{username}' уже существует."
            )
        return username

    def validate_email(self, email):
        duplicate_email = User.objects.filter(
            email=email
        ).exists()
        if duplicate_email:
            raise serializers.ValidationError(
                f"Почта '{email}' уже существует."
            )
        return email


class MePatchSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name", "last_name", "bio", "role",)
        model = User
        read_only_fields = ("role",)


class NewUserRegSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    def validate_username(self, username):
        return UserSerializer.validate_username(self, username)
    
    def validate_email(self, email):
        return UserSerializer.validate_email(self, email)
    
    def save(self):
        user = User(
            username=self.validated_data["username"],
            email = self.validated_data["email"],
        )
        user.save()
        return user


class GetJWTTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        lookup_field = "slug"
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        lookup_field = "slug"
        model = Genre


class GetTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True,)
    rating = serializers.IntegerField(
        read_only=True, source="reviews__score__avg",
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', "rating",)
        model = Title
        read_only_fields = ("id", "name", "year", "description" )

    def get_year(self, obj):
        if dt.datetime.now().year < obj.year:
            raise ValueError("Не правильно введен год")


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre", "category",)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='name'
    )

    class Meta:
        fields = ("id", "text", "title", "author", "score", "pub_date",)
        model = Review


    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        user = self.context['request'].user
        if Review.objects.filter(title=title, author=user):
            raise serializers.ValidationError(
                'Нельзя оставить больше одного отзыва.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )
    review = serializers.SlugRelatedField(
        slug_field="text", read_only=True,
    )
    class Meta:
        fields = ("id", "author", "review", "text", "pub_date",)
        model = Comment
