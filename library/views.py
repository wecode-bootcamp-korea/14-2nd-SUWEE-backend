import json, requests
from datetime import date

from django.http      import JsonResponse
from django.views     import View
from django.db.models import (
        Sum,
        Count,
        Max,
)

from library.models   import Library, LibraryBook
from share.decorators import check_auth_decorator
from user.models      import (
        User,
        UserBook,
)
from book.models      import (
        Book,
)


class MyLibraryView(View):
    @check_auth_decorator
    def post(self,request):
        data = json.loads(request.body)
        try :
            user      = request.user
            book_id   = data['book_id']
            library   = Library.objects.filter(user_id=user)
            nickname  = User.objects.get(id=user).nickname

            if not library:
                library = Library.objects.create(
                    user_id = user,
                    name    = nickname
                )
                return JsonResponse({'message':'CREATED_LIBRARY'}, status=200)
            if LibraryBook.objects.filter(book_id=book_id, library_id=library.first().id).exists():
                return JsonResponse({'message':'ALREADY_BOOK'}, status=400)
            book_save  = LibraryBook.objects.create(
                book_id    = book_id,
                library_id = library.first().id
            )
            return JsonResponse({'book_save':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message':'INVAILD_KEYS'}, status=400)

class LibraryBookListView(View):
    @check_auth_decorator
    def get(self, request):
        user_id  = request.user
        ordering = request.GET.get('ordering', '1')

        conditions = {
            1 : '-created_at',
            2 : 'book__title',
            3 : 'book__author',
            4 : '-book__publication_date'
        }

        books = LibraryBook.objects.select_related(
            'book','library').filter(
                library__user_id=user_id).order_by(conditions[int(ordering)])

        book_list = {
            "libraryBook" : [{
                "id"     : library.book.id,
                "title"  : library.book.title,
                "image"  : library.book.image_url,
                "author" : library.book.author
            } for library in books]}
        return JsonResponse (book_list, status = 200)

class StatisticsView(View):
    @check_auth_decorator
    def get(self, request):
        result = {}

        # 사용자의 총 독서권수, 총 독서시간        
        userbook = UserBook.objects.select_related('user', 'book').filter(user_id = request.user)
        
        result['total_book_count'] = userbook.count()
        result['total_read_time']  = userbook.aggregate(total_read_time=Sum('time'))['total_read_time']
        if not result['total_read_time']:
            result['total_read_time'] = 0            
        
        # 추천 책 선정
        if not result['total_book_count']:
            result['recommand_book'] = list(Book.objects.all().order_by('-publication_date').values('id', 'title', 'image_url', 'author')[:1])[0]
        else:
            count_of_category = list(userbook.values('book__category_id').annotate(count = Count('book__category_id')))
            target            = max(count_of_category, key=lambda x:x['count'])
            category_id       = target['book__category_id']
                    
            books = Book.objects.filter(category_id=category_id).order_by('-publication_date')
            if books:
                result['recommand_book'] = list(books.values('id', 'title', 'image_url', 'author'))[0]
        
        return JsonResponse({"message":"SUCCESS", "data":result}, status=200)
