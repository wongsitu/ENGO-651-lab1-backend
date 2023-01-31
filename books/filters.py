from django_filters import rest_framework
from .models import Book

class BookFilter(rest_framework.FilterSet):
    id = rest_framework.CharFilter(field_name='id', lookup_expr='iexact')
    isbn = rest_framework.CharFilter(field_name='isbn', lookup_expr='icontains')
    title = rest_framework.CharFilter(field_name='title', lookup_expr='icontains')
    author = rest_framework.CharFilter(field_name='author', lookup_expr='icontains')
    year = rest_framework.CharFilter(field_name='year', lookup_expr='icontains')