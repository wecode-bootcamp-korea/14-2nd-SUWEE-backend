from django.urls import path
from .views      import RecentlyBookView

urlpatterns = [
    path('/recently', RecentlyBookView.as_view())
]

