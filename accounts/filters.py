from django_filters.rest_framework import  FilterSet, NumberFilter
from .models import User

class ContractorFilter(FilterSet):
    min_rate = NumberFilter(field_name='avg_rate', lookup_expr='gte') 
    min_done_ads = NumberFilter(field_name='done_ads_count', lookup_expr='gte')

    class Meta:
        model = User
        fields = ['min_rate', 'min_done_ads']