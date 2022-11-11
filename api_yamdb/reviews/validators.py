import datetime
import re

from django.core.exceptions import ValidationError


def validate_year(year):
    if year > datetime.datetime.now().year:
        raise ValidationError(
            (f'Введнный {year} год больше текущего!')
        )


def validate_slug(slug):
    if re.search(r'^[-a-zA-Z0-9_]+$', slug) is None:
        raise ValidationError(
            f'{slug} не подходит. Может содержать латинские буквы, цифрыб'
            f'и спецсимвол _'
        )
