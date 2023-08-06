import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _
from utilities.filters import MultiValueCharFilter
from netbox.filtersets import BaseFilterSet
from .models import CiscoDeviceSupport, CiscoDeviceTypeSupport


class CiscoDeviceSupportFilterSet(BaseFilterSet):
    recommended_release = MultiValueCharFilter(
        lookup_expr="iexact"
    )

    desired_release = MultiValueCharFilter(
        lookup_expr="iexact"
    )

    current_release = MultiValueCharFilter(
        lookup_expr="iexact"
    )

    sr_no_owner =  django_filters.BooleanFilter(
        required=False,
    )

    is_covered =  django_filters.BooleanFilter(
        required=False,
    )

    eox_has_error =  django_filters.BooleanFilter(
        required=False,
    )

    class Meta:
        model = CiscoDeviceSupport
        fields = ("id", "sr_no_owner", "is_covered", "eox_has_error",)
