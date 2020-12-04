import json
from django.views   import View
from django.http    import JsonResponse

from .models        import Book, Category, Keyword, Today, Review, Like
from library.models import Library, LibraryBook
from user.models    import UserBook




class BookDetailView(View):
    def get(self, request, book_id):
        try :
            book = Book.objects.select_related('category').prefetch_related('review_set').get(id=book_id)
            book_detail = {
                'title'            : book.title,
                'subtitle'         : book.subtitle,
                'image_url'        : book.image_url,
                'company'          : book.company,
                'author'           : book.author,
                'contents'         : book.contents,
                'company_review'   : book.company_review,
                'page'             : book.page,
                'publication_date' : book.publication_date,
                'description'      : book.description,
                'category'         : book.category.name,
                'review_count'     : book.review_set.count(),
                'reder'            : book.userbook_set.count()
                }
            return JsonResponse({'book_detail':book_detail}, status =200)
        except Book.DoesNotExist:
            return JsonResponse({'message':'NOT_EXIST_BOOK'}, status =400)

    def post(self,request, book_id):
        data = json.loads(request.body)
        try:
            user = data['user_id']
            libraries = Library.objects.filter(user_id=user)

            if not libraries:
                return JsonResponse({'message':'NOT_EXITS_LIBRARY'}, status=400)

                book_save  = LibraryBook.objects.create(
                book_id    = book_id,
                library_id = libraries.first().id
                 )
            return JsonResponse({'book_save':'SUCCESS'}, status =200)
        except Book.DoesNotExist:
            return JsonResponse({'message':'NOT_EXIST_BOOK'}, status =400)


