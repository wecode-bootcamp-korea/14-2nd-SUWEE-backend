from django.urls     import path
from .views          import (
    RecentlyBookView,
    BookDetailView,
    SearchBookView,
    CommingSoonBookView,
    BestSellerBookView,
    ReviewView,
    ReviewLikeView
)

urlpatterns = [
    path('/recently', RecentlyBookView.as_view()),
    path('/<int:book_id>', BookDetailView.as_view()),
    path('/search', SearchBookView.as_view()),
    path('/commingsoon', CommingSoonBookView.as_view()),
    path('/bestseller', BestSellerBookView.as_view()),
    path('/<int:book_id>/review',ReviewView.as_view()),
    path('/reviewlike', ReviewLikeView.as_view())
]
