import json
from datetime         import timedelta, date

from django.views     import View
from django.http      import JsonResponse

from .models          import Book


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
