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

    def get_queryset(self, search, *args, **kwargs):
        query = 'SELECT * from books_book'
        if (search):
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM books_book 
                                WHERE LOWER(title) LIKE %s 
                                OR LOWER(isbn) LIKE %s 
                                OR LOWER(author) LIKE %s""",
                                ['%' + search + '%', '%' + search + '%', '%' + search + '%'])
                response = cursor.fetchall()
                return Book.objects.filter(pk__in=[book[0] for book in response])
        return Book.objects.raw(query)

    def list(self, request, *args, **kwargs):
        search = request.GET.get('search')
        queryset = self.filter_queryset(self.get_queryset(search=search))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM books_book WHERE id = %s", [pk])
            (id, isbn, title, author, year) = cursor.fetchone()

            return Response({ 'id': id, 'isbn': isbn, 'title': title, 'author': author, 'year': year })
