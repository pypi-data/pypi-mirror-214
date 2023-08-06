from collections import defaultdict
from django.utils.translation import gettext_lazy
from netbox.views import generic
from . import models, tables


class CiscoDeviceSupportListView(generic.ObjectListView):
    queryset = models.CiscoDeviceSupport.objects.all()
    table = tables.CiscoDeviceSupportTable
    actions = ("export", "delete", "bulk_delete")
    # action_perms = defaultdict(set, **{"bulk_delete": {"delete"}})


class CiscoDeviceSupportDeleteView(generic.ObjectDeleteView):
    queryset = models.CiscoDeviceSupport.objects.all()


class CiscoDeviceSupportBulkDeleteView(generic.BulkDeleteView):
    queryset = models.CiscoDeviceSupport.objects.all()
    # filterset = filtersets.CiscoDeviceSupportFilterSet
    table = tables.CiscoDeviceSupport


class CiscoDeviceTypeSupportListView(generic.ObjectListView):
    queryset = models.CiscoDeviceTypeSupport.objects.all()
    table = tables.CiscoDeviceTypeSupportTable
    actions = ("export", "bulk_delete")
    action_perms = defaultdict(set, **{"bulk_delete": {"delete"}})
