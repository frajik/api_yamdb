from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from Users.models import User

from .validators import validate_slug, validate_year


class Category(models.Model):
    """Категории (типы) произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название категории"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=(validate_slug,)
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Категории жанров."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название жанра"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=(validate_slug,)
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения, к которым пишут отзывы."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название произведения"
    )
    year = models.IntegerField(
        verbose_name="Дата выхода",
        validators=(validate_year,)
    )
    description = models.TextField(
        verbose_name="Описание "
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        verbose_name="Жанр"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="titles",
        verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы на произведения."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Заголовок отзыва"
    )
    text = models.TextField(
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Автор отзыва"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации отзыва"

    )
    score = models.PositiveIntegerField(
        verbose_name="Рейтинг",
        validators=[
            MinValueValidator(1, "Значение должно быть от 1 до 10"),
            MaxValueValidator(10, "Значение должно быть от 1 до 10")
        ]
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [models.UniqueConstraint(
            fields=["title", "author"],
            name="unique_reviews"
        ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарии на отзывы."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        max_length=200,
        verbose_name="Отзыв"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Автор комментария"
    )
    text = models.TextField(
        max_length=200,
        verbose_name="Текст комментария",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации комментария"
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text
