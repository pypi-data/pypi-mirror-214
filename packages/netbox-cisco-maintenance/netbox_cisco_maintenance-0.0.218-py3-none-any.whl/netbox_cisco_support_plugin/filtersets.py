from django.db.models import Q
from django.utils.translation import gettext as _

import django_filters

from netbox.filtersets import BaseFilterSet
from .models import CiscoDeviceSupport, CiscoDeviceTypeSupport


class CiscoDeviceSupportFilterSet(BaseFilterSet):
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
        fields = ("sr_no_owner", "is_covered", "eox_has_error",)
