from django.db.models import Q
from django.utils.translation import gettext as _

import django_filters

from netbox.filtersets import BaseFilterSet
from .models import CiscoDeviceSupport, CiscoDeviceTypeSupport


class CiscoDeviceSupportFilterSet(BaseFilterSet):
    eox_has_error =  django_filters.BooleanFilter(
        required=False,
    )

    class Meta:
        model = CiscoDeviceSupport
        fields = ("eox_has_error",)
