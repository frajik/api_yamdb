from csv import DictReader
from django.core.management import BaseCommand

from ...models import Title

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the Title data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from csv file"

    def handle(self, *args, **options):

        if Title.objects.exists():
            print('data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return

        print("Loading data")

        for row in DictReader(open('static/data/titles.csv')):
            title = Title(id=row['id'], name=row['name'], year=row['year'], category=row['category'])
            title.save()
