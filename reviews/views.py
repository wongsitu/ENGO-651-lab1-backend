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
            review = review_form.save(commit=False)
            isbn = request.data.get('isbn')
            book = Book.objects.get(isbn=isbn)
            review.user = request.user
            review.book = book
            review.save()
            return Response({ 'success': True, 'data': model_to_dict(review) })
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