import json
from datetime       import timedelta, date

from django.views   import View
from django.http    import JsonResponse

from .models        import Book, Category, Keyword, Today, Review, Like
from library.models import Library, LibraryBook
from user.models    import UserBook


class RecentlyBookView(View):
    def get (self, request):
        day    = request.GET.get('day')
        limit  = request.GET.get('limit', '20')

        today          = date.today()
        previous_days  = today - timedelta(days=int(day))

        books = [{
            "title"  : book.title,
            "image"  : book.image_url,
            "author" : book.author
        } for book in (Book.objects.filter(
            publication_date__range=[previous_days,today])
            .order_by('-publication_date')[:int(limit)])]
        return JsonResponse({"oneMonthBook":books}, status=200)

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
            return JsonResponse({'book_detail':book_detail}, status=200)
        except Book.DoesNotExist:
            return JsonResponse({'message':'NOT_EXIST_BOOK'}, status=400)

