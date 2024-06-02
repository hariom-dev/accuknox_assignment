from django_filters import rest_framework
from django.contrib.auth import get_user_model
from django.db.models import Q


class UserFilter(rest_framework.FilterSet):
    search = rest_framework.CharFilter(method='name_filter')
    
    class Meta:
        model = get_user_model()
        fields = ['search']
    
    def name_filter(self, queryset, name, value):
        return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(email__exact=value))