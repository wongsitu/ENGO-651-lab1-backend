from django import forms
from reviews.models import Review

class ReviewForm(forms.ModelForm):
    isbn = forms.CharField(required=True)

    class Meta():
        model = Review
        fields = ('title','description', 'rating')