from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Comment, Review, Title, Category, Genre,
from Users.models import User
from rest_framework.relations import SlugRelatedField


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