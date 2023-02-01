from django.urls import path
from .views import RegisterView, GetCSRFToken, LoginView, LogoutView, CurrentUserView

urlpatterns = [
    path('current_user', CurrentUserView.as_view()),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('csrf_cookie', GetCSRFToken.as_view())
]