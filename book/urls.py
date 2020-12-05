from django.urls     import path
from .views          import (
    TodayBookView,
    RecentlyBookView,
    BookDetailView,
    SearchBookView,
    CommingSoonBookView,
    BestSellerBookView,
    RecommendBookView,
    ReviewView,
    ReviewLikeView
)

urlpatterns = [
    path('/today', TodayBookView.as_view()),
    path('/recently', RecentlyBookView.as_view()),
    path('/<int:book_id>', BookDetailView.as_view()),
    path('/bestseller', BestSellerBookView.as_view()),
    path('/search', SearchBookView.as_view()),
    path('/commingsoon', CommingSoonBookView.as_view()),
    path('/<int:book_id>/review',ReviewView.as_view()),
    path('/reviewlike', ReviewLikeView.as_view()),
    path('/recommend', RecommendBookView.as_view())
]
