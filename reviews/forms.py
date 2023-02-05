from django import forms
from reviews.models import Review

class ReviewForm(forms.ModelForm):
    book = forms.CharField(required=True)

    class Meta():
        model = Review
        fields = ('title','description', 'rating')