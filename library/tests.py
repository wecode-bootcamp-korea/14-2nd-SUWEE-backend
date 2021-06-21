import jwt, json
from unittest.mock import patch, MagicMock
from random        import randint

from django.test   import TestCase, Client

from .models       import Library, LibraryBook
from user.models   import User,UserBook
from book.models   import (
    Book,
    Category,
    Review,
    Like,
)

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


class LibraryBookListTest(TestCase):
    maxDiff = None
    def setUp(self):

        client = Client()

        body = {
            "nickname"     : "burgundy",
            "phone_number" : "01049532184",
            "password"     : "a1234567890!"
        }

        response = client.post('/user/sign_up', json.dumps(body),
                               content_type='application/json')

        body = {
            "phone_number" : "01049532184",
            "password"     : "a1234567890!"
        }

        response = client.post('/user/sign_in', json.dumps(body),
                               content_type='application/json')

        self.token   = response.json()['access_token']
        self.headers = {'HTTP_Authorization': self.token}
        self.user    = User.objects.get(phone_number="01049532184")

        Book.objects.create(
            id                   = 1,
            title                = '안녕 고맛나',
            image_url            = "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
            company              = "맛밤",
            author               = "고수희",
            page                 = 804,
            publication_date     = "2020-12-31",
            )

        Book.objects.create(
            id                   = 2,
            title                = '파이를 햇볕에 쬐면 파이썬',
            image_url            = "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
            company              = "맛톨",
            author               = "수희고",
            page                 = 804,
            publication_date     = "2020-12-30",
            )


        Book.objects.create(
            id                   = 3,
            title                = '백엔드냐 프론트냐 그것이 문제로다',
            image_url            = "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
            company              = "밤나",
            author               = "원장님",
            page                 = 804,
            publication_date     = "2020-12-29",
            )

        Library.objects.create(
            id        = 1,
            user_id   = self.user.id,
            name      = "이사갈 서재",
            image_url = "https://files.slack.com/files-tmb/TH0U6FBTN-F01G8AKDEGN-b883ff5e83/1600907077321_720.jpg"
        )

        librarybook1 = LibraryBook.objects.create(
            id         = 1,
            library_id = 1,
            book_id    = 1
        )

        librarybook2 = LibraryBook.objects.create(
            id         = 2,
            library_id = 1,
            book_id    = 2
        )

        LibraryBook.objects.create(
            id         = 3,
            library_id = 1,
            book_id    = 3
        )

    def tearDown(self):
        Book.objects.all().delete()
        User.objects.all().delete()
        Library.objects.all().delete()
        LibraryBook.objects.all().delete()

    def test_librarybooklist_get_success_ordering_1(self):
        client   = Client()
        response = client.get('/library/books/1',
                              content_type = 'application/json', **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             "libraryBook":
                             [{
                                 "id"            : 3,
                                 "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                 "title"         : "백엔드냐 프론트냐 그것이 문제로다",
                                 "author"        : "원장님"
                             },
                                 {
                                     "id"            : 2,
                                     "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "title"         : "파이를 햇볕에 쬐면 파이썬",
                                     "author"        : "수희고"
                                 },
                                 {
                                     "id"            : 1,
                                     "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "title"         : "안녕 고맛나",
                                     "author"        : "고수희"
                                 }
                             ]
                         })

    def test_librarybooklist_get_success_ordering_2(self):
        client   = Client()
        response = client.get('/library/books/1?ordering=2',
                              content_type = 'application/json', ** self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             "libraryBook":
                             [{
                                 "id"            : 3,
                                 "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                 "title"         : "백엔드냐 프론트냐 그것이 문제로다",
                                 "author"        : "원장님"
                             },
                                 {
                                     "id"            : 1,
                                     "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "title"         : "안녕 고맛나",
                                     "author"        : "고수희"
                             },
                                 {
                                     "id"            : 2,
                                     "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "title"         : "파이를 햇볕에 쬐면 파이썬",
                                     "author"        : "수희고"
                                 },
                             ]
                         })

    def test_librarybooklist_get_success_ordering_3(self):
        client   = Client()
        response = client.get('/library/books/1?ordering=3',
                              content_type = 'application/json', ** self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             "libraryBook":
                             [{
                                 "id"            : 1,
                                 "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                 "title"         : "안녕 고맛나",
                                 "author"        : "고수희"
                             },
                                 {
                                     "id"            : 2,
                                     "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "title"         : "파이를 햇볕에 쬐면 파이썬",
                                     "author"        : "수희고"

                                 },
                                 {
                                     "id"            : 3,
                                     "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "title"         : "백엔드냐 프론트냐 그것이 문제로다",
                                     "author"        : "원장님"
                                 }
                             ]
                         })

    def test_librarybooklist_get_success_ordering_4(self):
        client   = Client()
        response = client.get('/library/books/1?ordering=4',
                              content_type = 'application/json', ** self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             "libraryBook":
                             [{
                                 "id"            : 1,
                                 "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                 "title"         : "안녕 고맛나",
                                 "author"        : "고수희"
                             },
                                 {
                                     "id"            : 2,
                                     "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "title"         : "파이를 햇볕에 쬐면 파이썬",
                                     "author"        : "수희고"

                                 },
                                 {
                                     "id"            : 3,
                                     "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "title"         : "백엔드냐 프론트냐 그것이 문제로다",
                                     "author"        : "원장님"
                                 }
                             ]
                         })

    def test_librarybooklist_get_not_found(self):
        client = Client()
        LibraryBook.objects.all().delete()

        response = client.get('/library/books/1',
                              content_type='application/json', **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             "libraryBook":[]
                         }
                        )

class LibraryTest(TestCase):
    def setUp(self):
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

        body       = {
                        'phone_number':'01027287069',
                        'password':'Passw0rd!',
                        'nickname':'추린'
                     }
        response   = self.client.post(
                            '/user/sign_up',
                            json.dumps(body),
                            content_type='application/json',
                        )

        self.user  = User.objects.get(phone_number='01027287069')
        body       = {
                        'phone_number':self.user.phone_number,
                        'password':'Passw0rd!',
                     }

        response   = self.client.post(
                            '/user/sign_in',
                            json.dumps(body),
                            content_type='application/json',
                        )

        self.token = response.json()['access_token']

        self.category = Category.objects.create(
            name = 'category'
        )

        books = [
                Book(
                    id               = i,
                    title            = self.DUMMY_TITLE,
                    image_url        = f'{self.DUMMY_IMAGE_URL}_{i}',
                    subtitle         = self.DUMMY_SUBTITLE,
                    company          = self.DUMMY_COMPANY,
                    author           = self.DUMMY_AUTHOR,
                    contents         = self.DUMMY_CONTENT,
                    company_review   = self.DUMMY_COMPANY_REVIEW,
                    page             = self.DUMMY_PAGE,
                    publication_date = self.DUMMY_PUBLICATION_DATE,
                    description      = self.DUMMY_DESCRIPTION,
                    category_id      = self.category.id) for i in range(1, 60)]

        Book.objects.bulk_create(books)

        UserBook.objects.bulk_create(
                [
                    UserBook(
                        user_id = self.user.id,
                        book_id = i, 
                        page=randint(0, 300), 
                        time=randint(10, 400)
                        ) for i in range(1, 5)
                ]
        )


    def tearDown(self):
        Book.objects.all().delete()

    def test_statistic_view_get_success(self):
        headers = {'HTTP_Authorization':self.token}
        response = self.client.get('/library/statistics',
                                    **headers)

        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json(), {})


class LibraryInfoTest(TestCase):

    def setUp(self):
        client = Client()

        body = {
            "nickname"     : "burgundy",
            "phone_number" : "01049532184",
            "password"     : "a1234567890!"
        }

        response = client.post('/user/sign_in', json.dumps(body),
                               content_type='application/json')

        self.token   = response.json()['access_token']
        self.headers = {'HTTP_Authorization': self.token}
        self.user    = User.objects.get(phone_number="01049532184")

        Book.objects.create(
            id                   = 1,
            title                = '안녕 고맛나',
            image_url            = "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
            company              = "맛밤",
            author               = "고수희",
            page                 = 804,
            publication_date     = "2020-12-31",
            )

        Book.objects.create(
            id                   = 2,
            title                = '파이를 햇볕에 쬐면 파이썬',
            image_url            = "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
            company              = "맛톨",
            author               = "수희고",
            page                 = 804,
            publication_date     = "2020-12-30",
            )


        Book.objects.create(
            id                   = 3,
            title                = '백엔드냐 프론트냐 그것이 문제로다',
            image_url            = "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
            company              = "밤나",
            author               = "원장님",
            page                 = 804,
            publication_date     = "2020-12-29",
            )

        Library.objects.create(
            id        = 1,
            user_id   = self.user.id,
            name      = "이사갈 서재",
            image_url = "https://files.slack.com/files-tmb/TH0U6FBTN-F01G8AKDEGN-b883ff5e83/1600907077321_720.jpg"
        )

        librarybook1 = LibraryBook.objects.create(
            id         = 1,
            library_id = 1,
            book_id    = 1
        )

        librarybook2 = LibraryBook.objects.create(
            id         = 2,
            library_id = 1,
            book_id    = 2
        )

        LibraryBook.objects.create(
            id         = 3,
            library_id = 1,
            book_id    = 3
        )

    def tearDown(self):
        Book.objects.all().delete()
        User.objects.all().delete()
        Library.objects.all().delete()
        LibraryBook.objects.all().delete()

    def test_librarybooklist_get_success_ordering_1(self):
        client   = Client()
        response = client.get('/library/books/1',
                              content_type = 'application/json', **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             "libraryBook":
                             [{
                                 "id"            : 3,
                                 "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                 "title"         : "백엔드냐 프론트냐 그것이 문제로다",
                                 "author"        : "원장님"
                             },
                                 {
                                     "id"            : 2,
                                     "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "title"         : "파이를 햇볕에 쬐면 파이썬",
                                     "author"        : "수희고"
                                 },
                                 {
                                     "id"            : 1,
                                     "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "title"         : "안녕 고맛나",
                                     "author"        : "고수희"
                                 }
                             ]
                         })

    def test_librarybooklist_get_success_ordering_2(self):
        client   = Client()
        response = client.get('/library/books/1?ordering=2',
                              content_type = 'application/json', ** self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             "libraryBook":
                             [{
                                 "id"            : 3,
                                 "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                 "title"         : "백엔드냐 프론트냐 그것이 문제로다",
                                 "author"        : "원장님"
                             },
                                 {
                                     "id"            : 1,
                                     "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "title"         : "안녕 고맛나",
                                     "author"        : "고수희"
                             },
                                 {
                                     "id"            : 2,
                                     "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "title"         : "파이를 햇볕에 쬐면 파이썬",
                                     "author"        : "수희고"
                                 },
                             ]
                         })

    def test_librarybooklist_get_success_ordering_3(self):
        client   = Client()
        response = client.get('/library/books/1?ordering=3',
                              content_type = 'application/json', ** self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             "libraryBook":
                             [{
                                 "id"            : 1,
                                 "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                 "title"         : "안녕 고맛나",
                                 "author"        : "고수희"
                             },
                                 {
                                     "id"            : 2,
                                     "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "title"         : "파이를 햇볕에 쬐면 파이썬",
                                     "author"        : "수희고"

                                 },
                                 {
                                     "id"            : 3,
                                     "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "title"         : "백엔드냐 프론트냐 그것이 문제로다",
                                     "author"        : "원장님"
                                 }
                             ]
                         })

    def test_librarybooklist_get_success_ordering_4(self):
        client   = Client()
        response = client.get('/library/books/1?ordering=4',
                              content_type = 'application/json', ** self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             "libraryBook":
                             [{
                                 "id"            : 1,
                                 "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                 "title"         : "안녕 고맛나",
                                 "author"        : "고수희"
                             },
                                 {
                                     "id"            : 2,
                                     "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "title"         : "파이를 햇볕에 쬐면 파이썬",
                                     "author"        : "수희고"

                                 },
                                 {
                                     "id"            : 3,
                                     "image"         : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "title"         : "백엔드냐 프론트냐 그것이 문제로다",
                                     "author"        : "원장님"
                                 }
                             ]
                         })

    def test_librarybooklist_get_not_found(self):
        client = Client()
        LibraryBook.objects.all().delete()

        response = client.get('/library/books/1',
                              content_type='application/json', **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             "libraryBook":[]
                         }
                        )

class LibraryTest(TestCase):
    def setUp(self):
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

        body       = {
                        'phone_number':'01027287069',
                        'password':'Passw0rd!',
                        'nickname':'추린'
                     }
        response   = self.client.post(
                            '/user/sign_up',
                            json.dumps(body),
                            content_type='application/json',
                        )

        self.user  = User.objects.get(phone_number='01027287069')
        body       = {
                        'phone_number':self.user.phone_number,
                        'password':'Passw0rd!',
                     }

        response   = self.client.post(
                            '/user/sign_in',
                            json.dumps(body),
                            content_type='application/json',
                        )

        self.token = response.json()['access_token']

        self.category = Category.objects.create(
            name = 'category'
        )

        books = [
                Book(
                    id               = i,
                    title            = self.DUMMY_TITLE,
                    image_url        = f'{self.DUMMY_IMAGE_URL}_{i}',
                    subtitle         = self.DUMMY_SUBTITLE,
                    company          = self.DUMMY_COMPANY,
                    author           = self.DUMMY_AUTHOR,
                    contents         = self.DUMMY_CONTENT,
                    company_review   = self.DUMMY_COMPANY_REVIEW,
                    page             = self.DUMMY_PAGE,
                    publication_date = self.DUMMY_PUBLICATION_DATE,
                    description      = self.DUMMY_DESCRIPTION,
                    category_id      = self.category.id) for i in range(1, 60)]

        Book.objects.bulk_create(books)

        UserBook.objects.bulk_create(
                [
                    UserBook(
                        user_id = self.user.id,
                        book_id = i, 
                        page=randint(0, 300), 
                        time=randint(10, 400)
                        ) for i in range(1, 5)
                ]
        )


    def tearDown(self):
        Book.objects.all().delete()

    def test_statistic_view_get_success(self):
        headers = {'HTTP_Authorization':self.token}
        response = self.client.get('/library/statistics',
                                    **headers)

        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json(), {})


class LibraryInfoTest(TestCase):

    def setUp(self):
        client = Client()

        body = {
            "nickname"     : "burgundy",
            "phone_number" : "01049532184",
            "password"     : "a1234567890!"
        }

        response = client.post('/user/sign_up', json.dumps(body),
                               content_type='application/json')

        body = {
            "phone_number" : "01049532184",
            "password"     : "a1234567890!"
        }

        response = client.post('/user/sign_in', json.dumps(body),
                               content_type='application/json')

        self.token   = response.json()['access_token']
        self.headers = {'HTTP_Authorization': self.token}
        self.user    = User.objects.get(phone_number="01049532184")
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

        update_user = User.objects.get(id=self.user.id)
        update_user.nickname = "신라면"
        update_user.save()

        Library.objects.create(
            id        = 1,
            user_id   = self.user.id,
            name      = "이사갈 서재",
            image_url = ""
        )

    def tearDown(self):
        User.objects.all().delete()
        Library.objects.all().delete()

        response = self.client.post(self.URL, content_type='application/json', **self.header)
        self.assertEqual(response.json()['message'] ,'INVAILD_KEYS')
        self.assertEqual(response.status_code, 400)
        response = self.client.post(self.URL, content_type='application/json')
        self.assertEqual(response.json()['message'] ,'INVAILD_KEYS')
        self.assertEqual(response.status_code, 400)




        Library.objects.create(
            id        = 1,
            user_id   = self.user.id,
            name      = "이사갈 서재",
            image_url = ""
        )

    def tearDown(self):
        User.objects.all().delete()
        Library.objects.all().delete()

    def test_libraryinfo_get_success(self):
        client   = Client()
        response = client.get('/1',
                              content_type = 'application/json', **self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             "libraryInfo":
                             [{
                                 "libraryName"  : "이사갈 서재",
                                 "libraryimage" : "",
                                 "userName"     : "신라면",
                                 "userImage"    : ""
                             }]
                         })
