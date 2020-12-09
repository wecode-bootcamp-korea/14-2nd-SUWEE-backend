import json, requests

from django.http      import JsonResponse
from django.views     import View

from share.decorators import check_auth_decorator
from library.models   import Library, LibraryBook
from book.models      import Book
from user.models      import User

from share.decorators import check_auth_decorator

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
