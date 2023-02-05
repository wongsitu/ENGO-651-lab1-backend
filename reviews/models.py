from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from books.models import Book

class Review(models.Model):
    RATING_CHOICES = (
      (1, '1'),
      (2, '2'),
      (3, '3'),
      (4, '4'),
      (5, '5'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    title = models.CharField(max_length=250, blank=False, name="title")
    description = models.TextField(max_length=1000, blank=True, name="description")
    created_at = models.DateTimeField(auto_now_add=True, name="created_at")
    updated_at = models.DateTimeField(auto_now=True, name="updated_at")
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, name="rating")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book')

    def __format__(self):
        return self.title