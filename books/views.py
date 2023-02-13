from books.models import Book
from rest_framework import viewsets, filters
from books.serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from books.filters import BookFilter
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import connection
import requests
from rest_framework import status

class Books(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def get_queryset(self, search=None, *args, **kwargs):
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
            cursor.execute("SELECT * FROM books_book WHERE isbn = %s", [pk])
            book = cursor.fetchone()

            res = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": f"isbn:{pk}"})
            data = res.json()

            if book:
                book_volume_info = data['items'][0]['volumeInfo']
                response = {
                            'id': book[0],
                            'isbn': book[1], 
                            'title': book[2], 
                            'author': book[3], 
                            'year': book[4], 
                            'average_rating': book_volume_info['averageRating'] if book_volume_info['averageRating'] else None,
                            'ratings_count': book_volume_info['ratingsCount'] if book_volume_info['ratingsCount'] else None,
                            'published_date': book_volume_info['publishedDate'] if book_volume_info['publishedDate'] else None
                            }
                for industry_identifier in book_volume_info['industryIdentifiers']:
                    response.update({ industry_identifier['type']: industry_identifier['identifier'] })
                return Response(response)
            return Response(status=status.HTTP_404_NOT_FOUND)