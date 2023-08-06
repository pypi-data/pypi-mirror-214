import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _
from utilities.filters import MultiValueCharFilter
from netbox.filtersets import BaseFilterSet
from .models import CiscoDeviceSupport, CiscoDeviceTypeSupport


class CiscoDeviceSupportFilterSet(BaseFilterSet):
    model = MultiValueCharFilter(lookup_expr="icontains")

    recommended_release = MultiValueCharFilter(lookup_expr="icontains")

    desired_release_status = django_filters.BooleanFilter(required=False)

    desired_release = MultiValueCharFilter(lookup_expr="iexact")

    current_release_status = django_filters.BooleanFilter(required=False)

    current_release = MultiValueCharFilter(lookup_expr="iexact")

    sr_no_owner = django_filters.BooleanFilter(required=False)

    is_covered = django_filters.BooleanFilter(required=False)

    coverage_end_date = django_filters.DateFilter()
    coverage_end_date__year = django_filters.DateFilter(field_name="coverage_end_date", lookup_expr="year")

    eox_has_error = django_filters.BooleanFilter(required=False)

    class Meta:
        model = CiscoDeviceSupport
        fields = ("id", "model", "sr_no_owner", "is_covered", "eox_has_error")
