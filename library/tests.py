import jwt, json
from django.test import TestCase, Client
from unittest.mock  import patch, MagicMock

from book.models import Book, Category, Review, Like
from user.models import UserBook, User
from .models     import Library, LibraryBook
import my_settings

class MyLibraryTestCase(TestCase):
    def setUp(self):
        self.URL = '/library/mylibrary'
        self.client = Client()

        self.DUMMY_NICKNAME         = 'hello'
        self.DUMMY_NICKNAME2        = 'hello2'

        self.DUMMY_LIBRARY_NAME     = 'library'
        self.DUMMY_LIBRARY_IMAGE_URL= 'unknown_image_url'

        self.DUMMY_TITLE            = 'title'
        self.DUMMY_IMAGE_URL        = 'image_url'
        self.DUMMY_COMPANY          = 'company'
        self.DUMMY_AUTHOR           = 'author'
        self.DUMMY_COMPANY_REVIEW   = 'company_review'
        self.DUMMY_PAGE             = 1
        self.DUMMY_PUBLICATION_DATE = '2020-02-22'
        self.DUMMY_DESCRIPTION      = 'description'
        self.DUMMY_CATEGORY         = 'category'

        self.category = Category.objects.create(
            name = self.DUMMY_CATEGORY
        )
        self.user = User.objects.create(
            nickname = self.DUMMY_NICKNAME
        )
        self.user2 = User.objects.create(
            id = 2,
            nickname = self.DUMMY_NICKNAME2
        )
        self.user3 = User.objects.create(
            id = 3,
            nickname = 'hi'
        )
        self.library  = Library.objects.create(
            user_id   = self.user.id,
            name      = self.DUMMY_LIBRARY_NAME,
            image_url = self.DUMMY_LIBRARY_IMAGE_URL
        )
        self.library2 = Library.objects.create(
            user_id   = self.user2.id,
            name      = self.DUMMY_LIBRARY_NAME,
            image_url = self.DUMMY_LIBRARY_IMAGE_URL
        )

        self.book = Book.objects.create(
            title            = self.DUMMY_TITLE,
            image_url        = self.DUMMY_IMAGE_URL,
            company          = self.DUMMY_COMPANY,
            author           = self.DUMMY_AUTHOR,
            company_review   = self.DUMMY_COMPANY_REVIEW,
            page             = self.DUMMY_PAGE,
            publication_date = self.DUMMY_PUBLICATION_DATE,
            description      = self.DUMMY_DESCRIPTION,
            category         = self.category,
        )
        self.library_book = LibraryBook.objects.create(
            library_id = self.library.id,
            book_id    = self.book.id
        )

        self.DUMMY_AUTH = jwt.encode(
            {'user_id':self.user.id},
            my_settings.SECRET_KEY['secret'],
            algorithm=my_settings.JWT_ALGORITHM
        ).decode('utf-8')

        self.header = {
            'HTTP_Authorization': self.DUMMY_AUTH
        }
        self.DUMMY_AUTH = jwt.encode(
            {'user_id':self.user.id},
            my_settings.SECRET_KEY['secret'],
            algorithm=my_settings.JWT_ALGORITHM
        ).decode('utf-8')

        self.header = {
            'HTTP_Authorization': self.DUMMY_AUTH
        }

    def tearsDown(self):
        pass

    def test_library_book_post_success(self):
        request = {
            'book_id'    : self.book.id,
        }
        token = jwt.encode({'user_id': User.objects.get(id=2).id}, my_settings.SECRET_KEY['secret'], algorithm=my_settings.JWT_ALGORITHM).decode('utf-8')
        response = self.client.post(self.URL,request, content_type='application/json', **{'HTTP_Authorization':token})
        self.assertEqual(response.json(),{'book_save': 'SUCCESS'})
        self.assertEqual(response.status_code, 200)

    def test_library_book_post_not_library_exist(self):
        request = {
            'book_id'    : self.book.id,
            'library_id' : None
        }
        token = jwt.encode({'user_id': User.objects.get(id=3).id}, my_settings.SECRET_KEY['secret'], algorithm=my_settings.JWT_ALGORITHM).decode('utf-8')
        response = self.client.post(self.URL,request, content_type='application/json', **{'HTTP_Authorization':token})
        self.assertEqual(response.json()['message'],'CREATED_LIBRARY')
        self.assertEqual(response.status_code, 200)

    def test_library_book_post_already_book(self):
        request = {
            'book_id'    : self.book.id
        }

        response = self.client.post(self.URL, request, content_type='application/json', **self.header)
        self.assertEqual(response.json(),{'book_save': 'SUCCESS'})
        self.assertEqual(response.status_code, 200)

    def test_library_book_post_not_exist_user(self):
        request = {
            'user_id'    : 0,
            'book_id'    : self.book.id,
        }

        response = self.client.post(self.URL, request, content_type='application/json')
        self.assertEqual(response.json()['message'],'NOT_EXIST_LIBRARY')
        self.assertEqual(response.status_code, 400)

    def test_library_book_post_already_book(self):
        request = {
            'user_id'    : self.user.id,
            'book_id'    : self.book.id
        }

        response = self.client.post(self.URL, request, content_type='application/json')
        self.assertEqual(response.json()['message'],'ALREADY_BOOK')
        self.assertEqual(response.status_code, 400)

    def test_library_book_post_fail(self):

        response = self.client.post(self.URL, content_type='application/json', **self.header)
        self.assertEqual(response.json()['message'] ,'INVAILD_KEYS')
        self.assertEqual(response.status_code, 400)
        response = self.client.post(self.URL, content_type='application/json')
        self.assertEqual(response.json()['message'] ,'INVAILD_KEYS')
        self.assertEqual(response.status_code, 400)





