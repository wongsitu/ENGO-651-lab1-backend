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

class Reviews(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

    def create(self, request):
        review_form = ReviewForm(data=request.data)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            book_id = request.data.get('book')
            book = Book.objects.get(id=book_id)
            review.user = request.user
            review.book = book
            review.save()
            return Response({ 'success': True, 'data': model_to_dict(review)  })
        else:
            return Response({ 'success': False, 'errors': review_form.errors })

    def get_queryset(self):
        query = 'SELECT * from reviews_review'
        return Review.objects.raw(query)

    def get_reviews_queryset(self, book_id, **kwargs):
        query = f"""SELECT * FROM reviews_review WHERE id = {book_id};"""
        return Review.objects.raw(query)
    
    def list(self, request, *args, **kwargs):
        book = request.GET.get('book')
        queryset = self.filter_queryset(self.get_queryset())
        if book:
            queryset = self.filter_queryset(self.get_reviews_queryset(book))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)