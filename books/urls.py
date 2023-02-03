from django.urls import path
from . import views

urlpatterns = [
  path('books', views.Books.as_view())
]