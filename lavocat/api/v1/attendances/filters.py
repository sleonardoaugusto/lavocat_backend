import django_filters

from lavocat.attendances.models import Attendance, ServicesOffered


class AttendanceFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(lookup_expr='icontains')
    document_id = django_filters.CharFilter(lookup_expr='startswith')
    services_provided = django_filters.MultipleChoiceFilter(
        lookup_expr='icontains', choices=ServicesOffered.choices
    )

    class Meta:
        model = Attendance
        fields = ['customer_name', 'document_id', 'services_provided']
