from django.urls import path
from .views      import MyLibraryView, LibraryBookListView

urlpatterns = [
    path('/mylibrary', MyLibraryView.as_view()),
    path('/books', LibraryBookListView.as_view())

]
