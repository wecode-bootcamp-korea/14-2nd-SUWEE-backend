from django.urls import path
from .views  import BookDetailView


urlpatterns = [
    path('/<int:book_id>', BookDetailView.as_view()),
    path('/save/<int:book_id>', BookDetailView.as_view()),

]
