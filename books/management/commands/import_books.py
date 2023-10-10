from typing import Any
from django.core.management.base import BaseCommand, CommandParser
import csv
from books.models import Book

class Command(BaseCommand):
    help = """
    Import Books from a csv file into database
    """
    
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('csv_file', type=str, nargs='?', help="Indicates the csv_file path to be loaded into database.\nMake sure to provide the full absolute path of the file")
        parser.add_argument('--v', action="store_true", help="Print a verbose output")
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        file = options['csv_file']
        try:
            with open(file, 'rt') as f:
                reader = csv.reader(f, delimiter=',')
                next(reader, None)
                count = 0
                for row in reader:
                    book = Book.objects.create(name=row[0], author=row[1], publisher=row[2], image=row[3], count=row[4])
                    count += 1
                    if options['v']:
                        self.stderr.write(self.style.SUCCESS(f'Added Book {book}'))
            self.stderr.write(self.style.SUCCESS(f'Successfully added {count} books'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))