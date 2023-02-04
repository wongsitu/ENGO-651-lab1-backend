from django.urls import path
from . import views

urlpatterns = [
  path('reviews', views.Reviews.as_view())
]