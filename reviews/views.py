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
            book_id = request.data.get('book')
            book = Book.objects.get(id=book_id)
            review.user = request.user
            review.book = book
            review.save()
            return Response({ 'success': True, 'data': model_to_dict(review)  })
        else:
            return Response({ 'success': False, 'errors': review_form.errors })