import django_filters

from src.attendances.models import Attendance, ServicesTypesOptions


class AttendanceFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(lookup_expr='icontains')
    document_id = django_filters.CharFilter(lookup_expr='startswith')
    services_types = django_filters.MultipleChoiceFilter(
        lookup_expr='icontains', choices=ServicesTypesOptions.choices
    )

    class Meta:
        model = Attendance
        fields = ['customer_name', 'document_id', 'services_types']
