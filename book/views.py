import json
import datetime
from datetime         import timedelta, date

from django.views     import View
from django.db        import transaction
from django.db.models import Q, Count
from django.http      import JsonResponse

from .models          import Book, Category, Keyword, Today, Review, Like
from library.models   import Library, LibraryBook
from user.models      import UserBook

from .modules.numeric import get_reading_numeric


class TodayBookView(View):
    def get (self, request):

        today = date.today().strftime('%Y-%m-%d')
        today_book =  Book.objects.prefetch_related(
            'review_set','review_set__like_set').filter(today__pick_date=today)

        if not today_book.exists():
            return JsonResponse({"message":"NO_BOOK"}, status = 400)

        today_review = today_book.first().review_set.prefetch_related(
            'like_set').values('user__nickname', 'user__image_url',
                               'contents').annotate(count=Count(
                                   'likes')).order_by('-count')[:1].first()

        book = [{
            "id"             : book.id,
            "title"          : book.title,
            "image"          : book.image_url,
            "author"         : book.author,
            "description"    : book.today_set.get(book_id=book).description,
            "reviewerName"   : today_review.get('user__nickname'),
            "reviewerImage"  : today_review.get('user__image_url')
                if today_review.get('user__image_url') is not None
                else '',
            "reviewContent"  : today_review.get('contents'),
        } for book in today_book]
        return JsonResponse({"todayBook":book}, status = 200)


class RecentlyBookView(View):
    def get (self, request):
        day    = request.GET.get('day', '30')
        limit  = request.GET.get('limit', '10')

        today          = date.today()
        previous_days  = today - timedelta(days=int(day))

        books = [{
            "id"     : book.id,
            "title"  : book.title,
            "image"  : book.image_url,
            "author" : book.author
            } for book in (Book.objects.filter(
                publication_date__range=[previous_days,today])
                .order_by('-publication_date')[:int(limit)])]

        if not books:
            return JsonResponse({"message":"NO_BOOKS"}, status=400)
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


class CommingSoonBookView(View):
    def get (self, request):
        day    = request.GET.get('day', '30')
        limit  = request.GET.get('limit', '10')

        today            = date.today()
        next_publication = today + timedelta(days=int(day))
        min_day          = today + timedelta(days=1)
        max_day          = today + timedelta(days=5)

        book_list = [{
            "id"     : book.id,
            "title"  : book.title,
            "image"  : book.image_url,
            "author" : book.author,
            "date"   : (book.publication_date - today).days
                if min_day <= book.publication_date <= max_day
                else book.publication_date.strftime('%m월%d')
        } for book in (Book.objects.filter(
            publication_date__range=[min_day, next_publication]).order_by
            ('publication_date')[:int(limit)])]

        if not book_list:
            return JsonResponse({"message":"NO_BOOKS"}, status=400)
        return JsonResponse({"commingSoonBook":book_list}, status=200)


class SearchBookView(View):
    def get(self, request):
        conditions = {
                'author__icontains'  : request.GET.get('author', ''),
                'title__icontains'   : request.GET.get('title', ''),
                'company__icontains' : request.GET.get('company', ''),
        }

        or_conditions = Q()

        for key, value in conditions.items():
            if value:
                or_conditions.add(Q(**{key: value}), Q.OR)

        if or_conditions:
            json_data = list(
                            Book.objects.filter(or_conditions).values(
                                'id',
                                'author',
                                'title',
                                'image_url',
                                'company'
                                )
                        )
            return JsonResponse({"message":"SUCCESS", "books":json_data}, status=200)

        return JsonResponse({"message":"INVALID_REQUEST"}, status=400)


class ReviewView(View):
    def post(self, request, book_id):
        data = json.loads(request.body)
        try :
            user_id  = data['user_id']
            contents = data['contents']

            if len(contents) < 200:
                review = Review.objects.create(
                    user_id  = user_id,
                    book_id  = book_id,
                    contents = contents
                )
                return JsonResponse({'message':'SUCCESS'}, status=200)
            return JsonResponse({'message':'LONG_CONTENTS'}, status=400)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    def get(self, request, book_id):
        data = json.loads(request.body)
        try:
            user_id = data['user_id']
            reviews = Review.objects.select_related('user').get(user_id=user_id)
            reviews = Review.objects.select_related('user').filter(user_id=user_id)
            review_list = [{
                'review_id'  : review.id,
                'nick_name'  : review.user.nickname,
                'user_img'   : review.user.image_url,
                'content'    : review.contents,
                'created_at' : review.created_at.strftime('%Y.%m.%d'),
            } for review in reviews ]
            return JsonResponse({'review_list':review_list}, status=200)
        except Review.DoesNotExist:
            return JsonResponse({'message':'NOT_EXIST_REVIEW'}, status=400)

    def delete(self, request, book_id):
        data = json.loads(request.body)
        try :
            user_id = data['user_id']
            review_id = request.GET['review_id']
            review  = Review.objects.get(id=review_id)
            if review.user_id == user_id:
                review.delete()
                return JsonResponse({'meassage':'SUCCESS'}, status=200)
            return JsonResponse({'meassage':'UNAUTHORIZED'}, status=400)
        except Review.DoesNotExist:
            return JsonResponse({'message':'NOT_EXIST_REVIEW'}, status=400)


class ReviewLikeView(View):
    def patch(self, request):
        data = json.loads(request.body)
        try:
            user_id    = data['user_id']
            review_id  = data['review_id']

            if Review.objects.filter(id=review_id).exists():
                like = Like.objects.get(user_id=user_id, review_id=review_id)
                like.delete()
                return JsonResponse({'message':'CANCEL'}, status=200)
            return JsonResponse({'meassage':'NOT_EXIST_REVIEW'}, status=400)
        except Like.DoesNotExist:
            Like.objects.create(user_id=user_id, review_id=review_id)
            return JsonResponse({'message':'SUCCESS'}, status=200)


class BestSellerBookView(View):
    def get (self, request):
        keyword = request.GET.get('keyword', '1')
        limit   = request.GET.get('limit', '10')

        if int(keyword) in range(2,7):
           books =  UserBook.objects.select_related('book').filter(
               book__keyword_id=int(keyword)).annotate(count=Count(
                   'book_id')).order_by('-count')[:int(limit)]
           if not books:
               return JsonResponse ({"message" : "NO_BOOKS"}, status = 400)

        else:
           books =  UserBook.objects.select_related('book').filter(
               book__keyword_id__gte=2).annotate(count=Count(
                   'book_id')).order_by('-count')[:int(limit)]
           if not books:
               return JsonResponse ({"message" : "NO_BOOKS"}, status = 400)

        book_list = [{
            "id"     : book.book.id,
            "title"  : book.book.title,
            "image"  : book.book.image_url,
            "author" : book.book.author
        } for book in books]
        return JsonResponse ({"bestSellerBook":book_list}, status=200)


class RecommendBookView(View):
    def get (self, request):
        keyword    = request.GET.get('keyword', '2')
        limit      = request.GET.get('limit', '6')

        today_iso  = datetime.datetime.now().isocalendar()
        year       = today_iso[0]
        week       = today_iso[1]
        day        = today_iso[2]

        week_start = date.fromisocalendar(year, week, 1)
        now        = datetime.datetime.now()

        books =  LibraryBook.objects.prefetch_related('book_set').filter(
            created_at__range=[week_start, now], book__keyword_id=int(
                keyword)).values('book_id', 'book__title', 'book__image_url',
                                'book__author').annotate(count=Count(
                    'book_id')).order_by('-count')[:int(limit)]

        book_list =[
            {
                "id": book.get('book_id'),
                "title" : book.get('book__title'),
                "image" : book.get('book__image_url'),
                "author" : book.get('book__author')
            } for book in books]

        if not book_list:
            return JsonResponse ({"message" : "NO_BOOKS"}, status=400)
        return JsonResponse ({"recommendBook":book_list}, status=200)
