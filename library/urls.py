from django.urls import path

from .views import (
    MyLibraryView
)

urlpatterns = [
    path('/mylibrary', MyLibraryView.as_view()),
]
