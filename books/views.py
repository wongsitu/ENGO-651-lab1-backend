from .models import Book
from rest_framework import viewsets, filters
from .serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class Books(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['isbn', 'title', 'author', 'year']
    filter_class = BookFilter