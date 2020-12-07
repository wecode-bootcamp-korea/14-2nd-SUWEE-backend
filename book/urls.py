from django.urls import path
from .views      import RecentlyBookView, BookDetailView

urlpatterns = [
    path('/recently', RecentlyBookView.as_view()),
    path('/<int:book_id>', BookDetailView.as_view()),
]

