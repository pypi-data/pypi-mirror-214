from django.db.models import Q
from django.utils.translation import gettext as _

import django_filters

from netbox.filtersets import BaseFilterSet
from .models import CiscoDeviceSupport, CiscoDeviceTypeSupport


class CiscoDeviceSupportFilterSet(BaseFilterSet):
    sr_no_owner =  django_filters.BooleanFilter(
        label=_("Serial Owner"),
        required=False,
    )

    is_covered =  django_filters.BooleanFilter(
        label=_("Is Covered"),
        required=False,
    )

    eox_has_error =  django_filters.BooleanFilter(
        label=_("Has EoX Error"),
        required=False,
    )

    class Meta:
        model = CiscoDeviceSupport
        fields = ("id", "sr_no_owner", "is_covered", "eox_has_error",)
