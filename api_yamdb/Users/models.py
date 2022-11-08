from django.contrib.auth.models import AbstractUser
from django.db import models

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"

ROLE_CHOICES = (
    (USER, "Аутенифицированный пользователь"),
    (MODERATOR, "Модератор"),
    (ADMIN, "Администратор")
)


class User(AbstractUser):
    """Модель пользователя."""
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Имя пользователя",
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name="Электронная почта"
    )
    first_name = models.CharField(max_length=150, blank=True,
                                  verbose_name="Имя")
    last_name = models.CharField(max_length=150, blank=True,
                                 verbose_name="Фамилия")
    bio = models.TextField(blank=True, verbose_name="Биография")
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name="Пользовательская роль",
    )

    def __str__(self):
        return f"Пользователь: {self.username}"

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR
