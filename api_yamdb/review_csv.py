from csv import DictReader
from django.core.management import BaseCommand

from ...models import Review

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the Review data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = "Loads data from csv file"

    def handle(self, *args, **options):

        if Review.objects.exists():
            print('data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return

        print("Loading data")

        for row in DictReader(open('static/data/review.csv')):
            review = Review(
                id=row['id'],
                title=row['title_id'],
                text=row['text'],
                author=row['author'],
                score=row['score'],
                pub_date=row['pub_date']
            )
            review.save()
