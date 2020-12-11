from django.urls import path

from .views import (
    MyLibraryView,
    StatisticsView,
    LibraryBookListView,
)

urlpatterns = [
    path('/mylibrary', MyLibraryView.as_view()),
    path('/statistics', StatisticsView.as_view()),
    path('/books', LibraryBookListView.as_view()),
]
