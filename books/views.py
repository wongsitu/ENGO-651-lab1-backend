from books.models import Book
from rest_framework import viewsets, filters
from books.serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from books.filters import BookFilter
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import connection

class Books(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer
    
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['isbn', 'title', 'author', 'year']
    filter_class = BookFilter
