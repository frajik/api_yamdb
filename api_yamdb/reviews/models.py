from django.db import models


class Category(models.Model):
    """Категории (типы) произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название категории"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
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
        unique=True
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural="Жанры"
    
    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения, к которым пишут отзывы."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название произведения"
    )
    year = models.IntegerField(
        verbose_name="Дата выхода"
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