import django_filters
from django_filters import DateFilter

from .models import *

class product_filter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    start_date = DateFilter(field_name='date_created', lookup_expr='lte')
    title = DateFilter(field_name='title', lookup_expr='icontains')
    class Meta:
        model = Products
        fields = '__all__'
        exclude = ['profile_pic']