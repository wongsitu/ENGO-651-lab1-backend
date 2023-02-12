from reviews.models import Review
from books.models import Book
from rest_framework import viewsets
from reviews.serializers import ReviewSerializer
from reviews.filters import ReviewFilter
from reviews.forms import ReviewForm
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django.db import connection
from rest_framework import status

class Reviews(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filter_class = ReviewFilter

    def create(self, request):
        review_form = ReviewForm(data=request.data)

        if review_form.is_valid():
            with connection.cursor() as cursor:
                isbn = request.data.get('isbn')
                user_id = request.user.id
                query = """
                    SELECT *
                    FROM reviews_review
                    INNER JOIN books_book
                    ON reviews_review.book_id = books_book.id
                    WHERE books_book.isbn = %s
                    AND reviews_review.user_id = %s
                """
                cursor.execute(query, [isbn, user_id])
                review = cursor.fetchone()

                if review:
                    return Response({ 'success': False, 'errors': ['You can only submit one review per book'] }, status=status.HTTP_208_ALREADY_REPORTED) 
                else:
                    title = review_form.data['title']
                    description = review_form.data['description']
                    rating = review_form.data['rating']
                    cursor.execute("SELECT * FROM books_book WHERE isbn = %s", [isbn])
                    book = cursor.fetchone()

                    query = """
                        INSERT INTO reviews_review 
                        (user_id, title, description, rating, book_id, created_at, updated_at) 
                        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
                        RETURNING user_id, title, description, rating, book_id, updated_at;
                    """

                    cursor.execute(query, (user_id, title, description, rating, book[0]))
                    (id, title, description, rating, book_id, created_at) = cursor.fetchone()

                    return Response({ 
                                    'success': True, 
                                    'data': { 
                                        'id': id, 
                                        'title': title, 
                                        'description': description, 
                                        'rating': rating, 
                                        'book_id': book_id, 
                                        'created_at': created_at 
                                        }
                                    })
        else:
            return Response({ 'success': False, 'errors': review_form.errors })

    def get_queryset(self, isbn, *args, **kwargs):
        query = 'SELECT * from reviews_review'
        if (isbn):
            with connection.cursor() as cursor:
                query = """
                    SELECT *
                    FROM reviews_review
                    INNER JOIN books_book
                    ON reviews_review.book_id = books_book.id
                    WHERE books_book.isbn = %s
                """
                cursor.execute(query, [isbn])
                response = cursor.fetchall()
                return Review.objects.filter(pk__in=[review[0] for review in response])
        return Review.objects.raw(query)

    def list(self, request, *args, **kwargs):
        isbn = request.GET.get('isbn')
        queryset = self.filter_queryset(self.get_queryset(isbn=isbn))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)