import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title
from Users.models import ROLE_CHOICES, User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\z', max_length=150)
    email = serializers.CharField(max_length=254)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    role = serializers.ChoiceField(
        choices=ROLE_CHOICES,
        default="user",
        required=False
    )

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

class NewUserRegSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.RegexField(regex=r'^[\w.@+-]+\z', max_length=150, required=True)

    def validate_username(self, username):
        return UserSerializer.validate_username(self, username)
    
    def validate_email(self, email):
        return UserSerializer.validate_email(self, email)


class GetJWTTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    # slug = SlugField(slug_field='category', read_only=True)

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    # slug = SlugField(slug_field='genre', read_only=True)

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(many=True, slug_field='name', read_only=True)
    category = SlugRelatedField(many=False, slug_field='name', read_only=True)
    rating = serializers.FloatField()

    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category')
        model = Title

    def get_year(self, obj):
        if dt.datetime.now().year < obj.year:
            raise ValueError("Не правильно введен год")


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='id'
    )
    score = serializers.IntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(10))
    )

    class Meta:
        fields = '__all__'
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
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
