from django.db.models import Q
from django.utils.translation import gettext as _

import django_filters

from netbox.filtersets import BaseFilterSet
from .models import CiscoDeviceSupport, CiscoDeviceTypeSupport


class CiscoDeviceSupportFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method="search",
        label=_("Search"),
    )

    class Meta:
        model = CiscoDeviceSupport
        fields = ("recommended_release", "desired_release", "current_release")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(user__username__icontains=value) | Q(name__icontains=value))
