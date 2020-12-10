import json,jwt
from unittest.mock  import patch, MagicMock
from datetime       import datetime
from django.test import TestCase, Client

import my_settings

from user.models import UserBook, User

from .models            import (
        Book,
        Category,
        Review,
        Like
)
from user.models        import (
        User,
        UserBook,
)
from .modules.numeric   import (
        get_reading_numeric,
)


class BookDetailTestCase(TestCase):
    maxDiff = None
    def setUp(self):
        self.URL = '/books/bookdetail/1'
        self.client = Client()

        self.DUMMY_TITLE            = 'title'
        self.DUMMY_IMAGE_URL        = 'image_url'
        self.DUMMY_SUBTITLE         = 'sub'
        self.DUMMY_COMPANY          = 'company'
        self.DUMMY_AUTHOR           = 'author'
        self.DUMMY_CONTENTS         = 'contents'
        self.DUMMY_COMPANY_REVIEW   = 'company_review'
        self.DUMMY_PAGE             = 1
        self.DUMMY_PUBLICATION_DATE = '2020-02-22'
        self.DUMMY_DESCRIPTION      = 'description'
        self.DUMMY_REDER            = 10

        self.DUMMY_CATEGORY         = 'category'

        self.category = Category.objects.create(
            id   = 1,
            name = 'category'
        )
        self.user = User.objects.create(
            id   = 1,
            nickname = 'hello'
        )

        self.book = Book.objects.create(
            id               = 1,
            title            = self.DUMMY_TITLE,
            image_url        = self.DUMMY_IMAGE_URL,
            subtitle         = self.DUMMY_SUBTITLE,
            company          = self.DUMMY_COMPANY,
            author           = self.DUMMY_AUTHOR,
            contents         = self.DUMMY_CONTENTS,
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

        self.DUMMY_AUTH = jwt.encode(
            {'user_id':self.user.id},
            my_settings.SECRET_KEY['secret'],
            algorithm=my_settings.JWT_ALGORITHM
        ).decode('utf-8')

        self.header = {
            'HTTP_Authorization': self.DUMMY_AUTH,
        }

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
                'contents'         : self.DUMMY_CONTENTS,
                'company_review'   : self.DUMMY_COMPANY_REVIEW,
                'page'             : self.DUMMY_PAGE,
                'publication_date' : self.DUMMY_PUBLICATION_DATE,
                'description'      : self.DUMMY_DESCRIPTION,
                'category'         : 'category',
                'review_count'     : 1,
                'reder'            : 1
                }})

    def test_book_get_fail(self):

        response = self.client.get('/books/bookdetail/2')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message':'NOT_EXIST_BOOK'})


class CommingSoonBookTest(TestCase):
    maxDiff = None
    def setUp(self):
        Book.objects.create(
            id               = 1,
            title            = '안녕 고맛나',
            image_url        = "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
            company          = "맛밤",
            author           = "고수희",
            page             = 804,
            publication_date = "2020-12-11"
        )

        Book.objects.create(
            id               = 2,
            title            = '안녕 고밤톨',
            image_url        = "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
            company          = "밤나",
            author           = "수희고",
            page             = 829,
            publication_date = "2020-12-31"
        )

    def tearDown(self):
        Book.objects.all().delete()

    def test_commingsoonbook_get_success(self):
        client   = Client()
        response = client.get('/books/commingsoon', content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             "commingSoonBook":
                             [{
                                 "id"     : 1,
                                 "title"  : "안녕 고맛나",
                                 "image"  : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                 "author" : "고수희",
                                 "date"   : 1
                             },
                                 {
                                     "id"     : 2,
                                     "title"  : "안녕 고밤톨",
                                     "image"  : "https://files.slack.com/files-pri/TH0U6FBTN-F01FTD2A9E3/20201205_140246.jpg",
                                     "author" : "수희고",
                                     "date"   : "12월31"
                                 }]
                         })

    def test_commingsoonbook_get_not_found(self):
        client = Client()
        Book.objects.all().delete()

        response = client.get('/books/commingsoon', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                         {
                             "message":"NO_BOOKS"
                         }
                        )

class BookTest(TestCase):
    def setUp(self):
        # 완독률/시간 수치 계산 test용 Data
        User.objects.create(id=1, nickname='test1')
        User.objects.create(id=2, nickname='test2')
        User.objects.create(id=3, nickname='test3')
        User.objects.create(id=4, nickname='test4')

        category = Category.objects.create(id=1, name='소설')
        Category.objects.create(id=2, name='수필')

        Book.objects.create(id=1, title='문은 닫혔다', page=300, author="김문주", publication_date=datetime.now(), category_id=1, company='늘빛출판사')
        Book.objects.create(id=2, title='그렇게 개발자가 되어간다', page=500, author="고수희", publication_date=datetime.now(), category_id=1, company='(주)위고두다')
        Book.objects.create(id=3, title='광수 생각', page=250, author="김광수", publication_date=datetime.now(), category_id=1, company='(주)늘빛')
        Book.objects.create(id=4, title='결전! 주식투자 2020', page=600, author="마광수", publication_date=datetime.now(), category_id=1, company='(주)한빛IT')
        Book.objects.create(id=5, title='니가 날?', page=100, author="마광수", publication_date=datetime.now(), category_id=2, company='ABCD')
        
        UserBook.objects.bulk_create([
            UserBook(user_id=1, book_id=1, page=129, time=130),
            UserBook(user_id=2, book_id=1, page=300, time=260),
            UserBook(user_id=3, book_id=1, page=159, time=30),
            UserBook(user_id=4, book_id=1, page=20, time=1130),
            UserBook(user_id=1, book_id=2, page=500, time=230),
            UserBook(user_id=1, book_id=3, page=250, time=90),
            UserBook(user_id=1, book_id=4, page=351, time=120),
            UserBook(user_id=1, book_id=5, page=0, time=0),
        ])

    def tearDown(self):
        Book.objects.all().delete()
        Category.objects.all().delete()

    def test_get_numeric_reading_success(self):
        data = get_reading_numeric(1)

        self.assertEqual(data['avg_finish'], 25.0)                                          
        self.assertEqual(data['expected_reading_minutes'], 260)                            
        self.assertEqual(data['category_avg_finish'], 3/7)                          
        self.assertEqual(data['category_expected_reading_minutes'], int((260+230+90)/3)) 

    def test_get_numeric_reading_not_exist(self):
        data = get_reading_numeric(-1)

        self.assertEqual(data, {"message":"NOT_EXIST"})

    def test_get_searched_books_all(self):
        target   = '주'
        response = self.client.get(
                        '/books/search',
                        {
                            'author':target,
                            'title':target,
                            'company':target,
                        }
                    )
        datas    = response.json()['books']
        
        for data in datas:
            result = target in data['title'] or target in data['author'] or target in data['company']
            self.assertTrue(result)
     
    def test_get_searched_books_with_author(self):
        target   = '고수희'
        response = self.client.get(
                        '/books/search',
                        {'author':target}
                    )
        datas    = response.json()['books']
       
        self.assertEqual(len(datas), 1)
        self.assertEqual(datas[0]['title'], '그렇게 개발자가 되어간다')

    def test_get_searched_books_with_title(self):
        target   = '결전'
        response = self.client.get(
                        '/books/search',
                        {'title':target}
                    )
        datas    = response.json()['books']

        self.assertEqual(len(datas), 1)
        self.assertEqual(datas[0]['title'], '결전! 주식투자 2020')
    
    def test_get_searched_books_with_company(self):
        target   = '빛'
        response = self.client.get(
                        '/books/search',
                        {'company':target}
                    )
        datas    = response.json()['books']

        self.assertEqual(len(datas), 3)
        self.assertEqual(datas[0]['company'], '늘빛출판사')
        self.assertEqual(datas[1]['company'], '(주)늘빛')
        self.assertEqual(datas[2]['company'], '(주)한빛IT')
        
    def test_get_searched_books_invalid_request(self):
        response = self.client.get(
                        '/books/search',  
                        {'wrong_key':'noname'}
                    )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"INVALID_REQUEST"})

class ReviewTestCase(TestCase):
    def setUp(self):
        self.URL = '/books/1/review'
        self.client = Client()


        self.DUMMY_TITLE            = 'title'
        self.DUMMY_SUBTITLE         = 'sub'
        self.DUMMY_COMPANY          = 'company'
        self.DUMMY_AUTHOR           = 'author'
        self.DUMMY_CONTENT          = 'content'
        self.DUMMY_COMPANY_REVIEW   = 'company_review'
        self.DUMMY_PAGE             = 1
        self.DUMMY_PUBLICATION_DATE = '2020-02-22'
        self.DUMMY_DESCRIPTION      = 'description'
        self.DUMMY_REDER            = 10
        self.DUMMY_CATEGORY         = 'category'

        self.DUMMY_NICKNAME         = 'hello'
        self.DUMMY_IMAGE_URL        = 'image_url'
        self.DUMMY_REVIEW_CONTENTS  = 'GOOD'
        self.DUMMY_REVIEW_DATE      = '2020.12.01'


        self.user = User.objects.create(
            id   = 1,
            nickname  = self.DUMMY_NICKNAME,
            image_url = self.DUMMY_IMAGE_URL

        )
        self.user2 = User.objects.create(
            id   = 2,
            nickname  = self.DUMMY_NICKNAME,
            image_url = self.DUMMY_IMAGE_URL

        )
        self.category = Category.objects.create(
            id   = 1,
            name = self.DUMMY_CATEGORY
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
            id         = 1,
            user_id    = self.user.id,
            book_id    = self.book.id,
            contents   = self.DUMMY_REVIEW_CONTENTS,
            created_at = '2020.12.01'
        )

        self.userbook = UserBook.objects.create(
            id   = 1,
            user_id = 1,
            book_id = 1,
            page= 1,
            time = 60 ,
        )

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

    def test_review_post_success(self):
        request = {
            'contents'  : self.DUMMY_REVIEW_CONTENTS
        }

        response = self.client.post(self.URL, request, content_type='application/json', **self.header)
        self.assertEqual(response.json(),{'message':'SUCCESS'})
        self.assertEqual(response.status_code, 200)

    def test_review_post_long_contents(self):
        request = {
            'contents' : 'gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg'
        }

        response = self.client.post(self.URL, request, content_type='application/json', **self.header)
        self.assertEqual(response.json()['message'],'LONG_CONTENTS')
        self.assertEqual(response.status_code, 400)

    def test_review_post_key_error(self):

        response = self.client.post(self.URL, content_type='application/json', **self.header)
        self.assertEqual(response.json()['message'],'KEY_ERROR')
        self.assertEqual(response.status_code, 400)

    def test_reivew_get_success(self):

        response = self.client.get(self.URL, **self.header)
        self.assertEqual(response.json(),{
            'review_list' :[{
                'review_id'  : self.reivew.id,
                'nick_name'  : self.DUMMY_NICKNAME,
                'user_img'   : self.DUMMY_IMAGE_URL,
                'content'    : self.DUMMY_REVIEW_CONTENTS,
                'created_at' : self.reivew.created_at.strftime('%Y.%m.%d')
            }]})
        self.assertEqual(response.status_code, 200)

    def test_authorbook_get_fail(self):

        response = self.client.get('/books/56623/review', **self.header)
        self.assertEqual(response.json(),{'message':'NOT_EXIST_BOOK'})
        self.assertEqual(response.status_code, 400)

    def test_reivew_delete_success(self):

        response = self.client.delete('/books/1/review?review_id=1', **self.header)
        self.assertEqual(response.json(),{'message':'SUCCESS'})
        self.assertEqual(response.status_code, 200)

    def test_reivew_delete_fail(self):

        response = self.client.delete('/books/1/review?review_id=200', **self.header)
        self.assertEqual(response.json(),{'message':'NOT_EXIST_REVIEW'})
        self.assertEqual(response.status_code, 400)

    def test_reivew_delete_not_this_user(self):

        token = jwt.encode({'user_id': User.objects.get(id=2).id}, my_settings.SECRET_KEY['secret'], algorithm=my_settings.JWT_ALGORITHM).decode('utf-8')
        response = self.client.delete('/books/1/review?review_id=1', **{'HTTP_Authorization':token})
        self.assertEqual(response.json(),{'message':'NOT_THIS_USER'})
        self.assertEqual(response.status_code, 400)

class ReviewLikeTestCase(TestCase):
    def setUp(self):
        self.URL = '/books/reviewlike'
        self.client = Client()


        self.DUMMY_TITLE            = 'title'
        self.DUMMY_SUBTITLE         = 'sub'
        self.DUMMY_COMPANY          = 'company'
        self.DUMMY_AUTHOR           = 'author'
        self.DUMMY_CONTENT          = 'content'
        self.DUMMY_COMPANY_REVIEW   = 'company_review'
        self.DUMMY_PAGE             = 1
        self.DUMMY_PUBLICATION_DATE = '2020-02-22'
        self.DUMMY_DESCRIPTION      = 'description'
        self.DUMMY_REDER            = 10
        self.DUMMY_CATEGORY         = 'category'

        self.DUMMY_NICKNAME         = 'hello'
        self.DUMMY_IMAGE_URL        = 'image_url'
        self.DUMMY_REVIEW_CONTENTS  = 'GOOD'
        self.DUMMY_REVIEW_DATE      = '2020.12.01'


        self.user = User.objects.create(
            id   = 1,
            nickname  = self.DUMMY_NICKNAME,
            image_url = self.DUMMY_IMAGE_URL

        )
        self.user2 = User.objects.create(
            id   = 2,
            nickname  = self.DUMMY_NICKNAME,
            image_url = self.DUMMY_IMAGE_URL

        )
        self.category = Category.objects.create(
            id   = 1,
            name = self.DUMMY_CATEGORY
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
            id         = 1,
            user_id    = self.user.id,
            book_id    = self.book.id,
            contents   = self.DUMMY_REVIEW_CONTENTS,
            created_at = '2020.12.01'
        )

        self.userbook = UserBook.objects.create(
            id   = 1,
            user_id = 1,
            book_id = 1,
            page= 1,
            time = 60 ,
        )

        self.like = Like.objects.create(
            id         = 1,
            user_id    = self.user.id,
            review_id  = self.book.id
        )

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

    def test_reviewlike_patch_cancel(self):
        request = {
            'review_id' : 1
        }

        response = self.client.patch(self.URL, request, content_type='application/json', **self.header)
        self.assertEqual(response.json(),{'message':'CANCEL'})
        self.assertEqual(response.status_code, 200)

    def test_reviewlike_patch_not_exist_review(self):
        request = {
            'review_id' : None
        }

        response = self.client.patch(self.URL, request, content_type='application/json', **self.header)
        self.assertEqual(response.json(),{'meassage':'NOT_EXIST_REVIEW'})
        self.assertEqual(response.status_code, 400)

    def test_reviewlike_patch_success(self):
        request = {
            'review_id' : 1
        }

        token = jwt.encode({'user_id': User.objects.get(id=2).id}, my_settings.SECRET_KEY['secret'], algorithm=my_settings.JWT_ALGORITHM).decode('utf-8')
        response = self.client.patch(self.URL,request, content_type='application/json', **{'HTTP_Authorization':token})
        self.assertEqual(response.json(),{'message':'SUCCESS'})
        self.assertEqual(response.status_code, 200)

