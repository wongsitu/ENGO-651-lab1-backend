from books.models import Book
import csv


def run():
    with open('scripts/books.csv') as file:
        reader = csv.reader(file)
        next(reader)

        Book.objects.all().delete()

        for row in reader:
            print(row)

            book = Book(isbn=row[0],
                        title=row[1],
                        author=row[2],
                        year=row[3]
                        )
            book.save()