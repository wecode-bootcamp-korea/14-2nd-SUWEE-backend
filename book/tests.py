import json
from django.views   import View
from django.http    import JsonResponse
from django.test    import TestCase, Client
from unittest.mock  import patch,MagicMock

from .models        import Book, Category, Keyword, Today, Review, Like
from library.models import Library, LibraryBook
from user.models    import UserBook, User

class BookDetailTest(TestCase):

    def setUp(self):

        User.objects.create(id = 10 , nickname ='hello')
        Category.objects.create(id =1, name='문학')
        self.book = Book.objects.create(
            id  = 1,
            title =  "1%의 글쓰기",
            subtitle = "1%의 글쓰기",
            image_url = "http://books.google.com/books/content?id=CTfvDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
            company= "Maekyung Publishing",
            author = "니시오카 잇세이",
            page= 196,
            publication_date= "2019-12-30",
            description ="description",
            category_id=1,
        )
        Review.objects.create(id=1, user_id=10, book_id=1,contents='good')
        Library.objects.create(id =1, name='서재', image_url='http://')
        LibraryBook.objects.create( book_id= 1, library_id = 1)

    def tearDown(self):
        Book.objects.all().delete()
        LibraryBook.objects.all().delete()

    def test_bookdetail_get_success(self):
        client = Client()
        print (self.book.id)
        response = client.get(f'/book/{self.book.id}')
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            'book_detail' : {
                "title" :  "1%의 글쓰기",
                "subtitle" : "subtitle",
                "image_url" : "http://books.google.com/books/content?id=CTfvDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                "company": "Maekyung Publishing",
                "author" : "니시오카 잇세이",
                "page:" : 196,
                "publication_date" : "2019-12-30",
                "description" : "글쓰기만 바꿔도 성적이 오른다 표현력과 사고력, 한꺼번에 잡는 최강의 쓰기 공식 우리 일상은 글쓰기로 넘쳐난다. 글쓰기라고 하면 에세이나 서평처럼 각 잡힌 글만 생각하는 경우가 많은데, 메일을 보내고 SNS로 누군가와 소통할 때도 우리는 글을 쓴다. 누군가에게 무언가를 설명할 때, 자신의 감상이나 의견을 피력할 때, 부탁하거나 사과할 때도 글쓰기가 필요하다. 빈도의 차이는 있겠지만 누구나 글을 쓰면서 살아간다. 그런데 생각보다 글쓰기를 어려워하는 사람이 많다. 내 딴에는 공 들여 문장을 다듬고 정확히 설명한다고 했는데, 누군가로부터 ‘지금 네가 무슨 말을 하는지 도통 모르겠다’는 말을 들은 적이 있다면 자신의 생각과 글쓰기를 점검해봐야 한다. 저자도 스스로 그런 사람이었다고 고백한다. 재수를 하면서 30년치 주요 대학의 입시문제를 풀고 시험에 대비했지만, 서술형으로 답안을 작성해야 하는 도쿄대의 특성을 제대로 이해하지 못해 또 다시 낙방했다. 문제를 풀 줄 알아도 그 과정을 상대에게 정확하게 글로 전달하지 못해 떨어졌다는 걸 깨닫고, 입시공부와 글쓰기 공부를 병행한다. 책을 읽고 글을 쓰면서 도쿄대에 지망하는 친구들의 글과 자신의 글을 비교하면서 둘 사이에 어떤 차이점이 있는지 확인한다. 그리고 매일매일 쓰고 또 썼다. 그렇게 습득한 글쓰기 비법이 ‘1%의 글쓰기’다. 나의 의견과 주장을 정확히 밝히되, 독자 입장에서 생각하면서 글을 써야 상대에게 의미가 전달된다는 것을 깨닫자 성적이 극적으로 상승했고 마침내 도쿄대에 합격하게 된다. 이 책은 단순한 글쓰기 책이 아니다. 같은 내용이라도 공부 잘하는 사람은 어떻게 생각하는지, 그리고 그것을 어떻게 정리해서 표현하는지를 밝힌 책이다. 상대가 이해해주겠지 막연하게 기대하는 글쓰기에서 벗어나 사고를 정교하게 다듬는 논리를 만드는 방법과 그것을 전략적으로 잘 이해시키는 표현력을 익힐 수 있게 돕는 책이다. 그래서 이 책을 따라 읽다보면 글쓰기뿐만 아니라 자연스럽게 공부머리도 기를 수 있다.",
                "category" :  "문학",
                "review_count" : 0,
                "reder" : 0
            }})

#    def test_bookdetail_get_fail(seif):
#        client = Client()
#
#        response = client.post('/book/1'), json.dumps(bookdetail), content_type='application/json'
#        self.assertEqual(response.status_code, 400)
#        self.assertEqual(response.json(),
#                         {'message':'NOT_EXIST_BOOK'})
#
#    def test_bookdetail_post_success(seif):
#        client = Client()
#
#        librarybook = {
#            'book_id' : '83',
#            'library_id' : '40' }
#
#        response = client.post('/book/save', json.dumps(bookdetail), content_type='application/json')
#        self.assertEqual(response.status_code, 201)
#        self.assertEqual(response.json(),
#                         {'book_save':'SUCCESS'})
#
#    def test_bookdetail_post_fail(seif):
#        client = Client()
#
#        librarybook = {
#            'book_id' : '',
#            'library_id' : '' }
#
#        response = client.post('/book/save', json.dumps(bookdetail), content_type='application/json')
#        self.assertEqual(response.status_code, 400)
#        self.assertEqual(response.json(),
#                        {'message':'NOT_EXIST_BOOK'})

# Create your tests here.
