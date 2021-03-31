import django_filters

from lavocat.attendances.models import Attendance, AttendanceStatus


class AttendanceFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(lookup_expr='icontains')
    document_id = django_filters.CharFilter(lookup_expr='startswith')
    status = django_filters.MultipleChoiceFilter(
        lookup_expr='in', choices=AttendanceStatus.choices
    )

    class Meta:
        model = Attendance
        fields = ['customer_name', 'document_id', 'status']
