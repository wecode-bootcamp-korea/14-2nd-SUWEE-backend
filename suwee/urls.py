from django.urls import path, include

urlpatterns = [
        path('books', include('book.urls')),
        path('user', include('user.urls')),
]
