from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from ..reviews.models import Category, Genre, Title


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