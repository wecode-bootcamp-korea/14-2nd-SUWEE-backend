import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "suwee.settings")
django.setup()

from user.models import User, UserBook
from book.models import Book, Category, Today, Like, Review
from library.models import Library, LibraryBook
from payment.models import Payment

csv_path = './csv_data/users.csv'
with open(csv_path) as csv_file:
    row = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        User.objects.create(nickname=row[0], phone_number=row[1], password=row[2], email=row[3], lmage_url=row[4])

csv_path = './csv_data/users_books.csv'
with open(csv_path) as csv_file:
    row = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        UserBook.objects.create(user_id=row[0], book_id=row[1], progress=row[2], time=row[3])

csv_path = './csv_data/reviews.csv'
with open(csv_path) as csv_file:
    row = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        Review.objects.create(user_id=row[0], book_id=row[1], contents=row[2])

csv_path = './csv_data/likes.csv'
with open(csv_path) as csv_file:
    row = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        Like.objects.create(review_id=row[0], user_id=row[1])


csv_path = './csv_data/libraries_books.csv'
with open(csv_path) as csv_file:
    row = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        LibraryBook_objects.create(library_id=row[0], book_id=row[1])


csv_path = './csv_data/libraries.csv'
with open(csv_path) as csv_file:
    row = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        Library.objects.create(user_id=row[0], name=row[1])


csv_path = './csv_data/categories.csv'
with open(csv_path) as csv_file:
    row = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        Category.objects.create(name=row[0])


csv_path = './csv_data/keywords.csv'
with open(csv_path) as csv_file:
    row = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        Keyword.objects.create(name=row[0])


csv_path = './csv_data/today.csv'
with open(csv_path) as csv_file:
    row = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        Today.objects.create(book_id=row[0], description=row[1])

csv_path = './csv_data/books.csv'
with open(csv_path) as csv_file:
    row = csv.reader(csv_file, delimiter=',')
    next(rows)
    for row in rows:
        Book.objects.create(
            title=row[0],
            subtitle=row[1],
            image_url=row[2],
            company=row[3],
            author=row[4],
            about_author=row[5],
            company_review=row[6],
            category_id=row[7],
            page=row[8],
            publication_date=row[9],
            description=row[10]
        )

print ('데이터베이스에 데이터 추가')
