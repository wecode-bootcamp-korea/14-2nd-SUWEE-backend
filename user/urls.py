from django.urls import path

from .views import (
            SignInView,
            SignUpView,
            SignInWithKakaoView,
        )

urlpatterns = [
        path('/sign_in', SignInView.as_view()),
        path('/sign_up', SignUpView.as_view()),
        path('/kakao_sign_in', SignInWithKakaoView.as_view()),
        ]
