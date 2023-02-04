from django_filters import rest_framework

class ReviewFilter(rest_framework.FilterSet):
    book = rest_framework.CharFilter(field_name='book__id', lookup_expr='iexact')