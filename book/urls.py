from django.urls import path

from .views import (
        RecentlyBookView,
        BookDetailView,
        SearchBookView,
        CommingSoonBookView,
)

urlpatterns = [
    path('/recently', RecentlyBookView.as_view()),
    path('/search', SearchBookView.as_view()),
    path('/<int:book_id>', BookDetailView.as_view()),
    path('/commingsoon', CommingSoonBookView.as_view())
]
