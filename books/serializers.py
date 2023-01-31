from .models import Book
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = ['id', 'isbn', 'title', 'author', 'year']