from django.contrib.auth.models import User
from reviews.models import Review
from rest_framework import serializers
from django.core import serializers as core_serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class ReviewSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = serializers.SerializerMethodField()

    def get_user(self, review):
        user = User.objects.get(id=review.user.id)
        serializer = UserSerializer(instance=user)
        return serializer.data

    class Meta:
        model = Review
        fields = ['id', 'user', 'title', 'description', 'created_at', 'updated_at', 'rating']