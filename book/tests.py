from django.test import TestCase, Client

from .models  import Book, Category, Review, Like
from user.models import UserBook, User


class BookDetailTestCase(TestCase):
    maxDiff = None
    def setUp(self):
        self.URL = '/books/1'
        self.client = Client()

        self.DUMMY_TITLE            = 'title'
        self.DUMMY_IMAGE_URL        = 'image_url'
        self.DUMMY_SUBTITLE         = 'sub'
        self.DUMMY_COMPANY          = 'company'
        self.DUMMY_AUTHOR           = 'author'
        self.DUMMY_CONTENT          = 'content'
        self.DUMMY_COMPANY_REVIEW   = 'company_review'
        self.DUMMY_PAGE             = 1
        self.DUMMY_PUBLICATION_DATE = '2020-02-22'
        self.DUMMY_DESCRIPTION      = 'description'
        self.DUMMY_REDER            = 10

        self.category = Category.objects.create(
            id   = 1,
            name = 'category'
        )
        self.user = User.objects.create(
            id   = 1,
            nickname = 'hello'
        )

        self.category = Category.objects.create(
            name = 'category'
        )

        self.book = Book.objects.create(
            id               = 1,
            title            = self.DUMMY_TITLE,
            image_url        = self.DUMMY_IMAGE_URL,
            subtitle         = self.DUMMY_SUBTITLE,
            company          = self.DUMMY_COMPANY,
            author           = self.DUMMY_AUTHOR,
            contents         = self.DUMMY_CONTENT,
            company_review   = self.DUMMY_COMPANY_REVIEW,
            page             = self.DUMMY_PAGE,
            publication_date = self.DUMMY_PUBLICATION_DATE,
            description      = self.DUMMY_DESCRIPTION,
            category_id      = 1,
        )
        self.reivew = Review.objects.create(
            id   = 1,
            user_id = 1,
            book_id = 1,
            contents = 'good'
        )
        self.userbook = UserBook.objects.create(
            id   = 1,
            user_id = 1,
            book_id = 1,
            page= 1,
            time = 60
        )

    def tearsDown(self):
        pass

    def test_book_get_success(self):

        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            'book_detail': {
                'title'            : self.DUMMY_TITLE,
                'subtitle'         : self.DUMMY_SUBTITLE,
                'image_url'        : self.DUMMY_IMAGE_URL,
                'company'          : self.DUMMY_COMPANY,
                'author'           : self.DUMMY_AUTHOR,
                'contents'         : self.DUMMY_CONTENT,
                'company_review'   : self.DUMMY_COMPANY_REVIEW,
                'page'             : self.DUMMY_PAGE,
                'publication_date' : self.DUMMY_PUBLICATION_DATE,
                'description'      : self.DUMMY_DESCRIPTION,
                'category'         : 'category',
                'review_count'     : 1,
                'reder'            : 1
                }})

    def test_book_get_fail(self):

        response = self.client.get('/books/2')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message':'NOT_EXIST_BOOK'})

