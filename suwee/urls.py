<<<<<<< HEAD
from django.urls import path,include

urlpatterns = [
    path('book', include('book.urls'))
=======
from django.urls import path, include

urlpatterns = [
    path('user', include('user.urls')),
    path('books', include('book.urls')),
    path('library', include('library.urls'))
>>>>>>> origin/master
]
