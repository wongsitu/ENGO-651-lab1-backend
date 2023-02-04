from reviews.models import Review
from rest_framework import viewsets
from reviews.serializers import ReviewSerializer
from reviews.filters import ReviewFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class Reviews(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filter_class = ReviewFilter