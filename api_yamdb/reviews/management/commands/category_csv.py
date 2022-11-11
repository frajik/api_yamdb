from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the Category data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from category.csv"

    def handle(self, *args, **options):

        if Category.objects.exists():
            print('data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return

        print("Loading data")

        for row in DictReader(
            open('static/data/category.csv', encoding='UTF-8')
        ):
            category = Category(
                id=row['id'], name=row['name'], slug=row['slug']
            )
            category.save()
