from collections import defaultdict
from django.utils.translation import gettext_lazy
from netbox.views import generic
from . import models, tables


#### Cisco Device Support ###################################################################################

class CiscoDeviceSupportListView(generic.ObjectListView):
    queryset = models.CiscoDeviceSupport.objects.all()
    table = tables.CiscoDeviceSupportTable
    actions = ("export", "delete", "bulk_delete")
    action_perms = defaultdict(set, **{"bulk_delete": {"delete"}})


class CiscoDeviceSupportDeleteView(generic.ObjectDeleteView):
    queryset = models.CiscoDeviceSupport.objects.all()


class CiscoDeviceSupportBulkDeleteView(generic.BulkDeleteView):
    queryset = models.CiscoDeviceSupport.objects.all()
    # filterset = filtersets.CiscoDeviceSupportFilterSet
    table = tables.CiscoDeviceSupport


#### Cisco Device Type Support ##############################################################################


class CiscoDeviceTypeSupportListView(generic.ObjectListView):
    queryset = models.CiscoDeviceTypeSupport.objects.all()
    table = tables.CiscoDeviceTypeSupportTable
    actions = ("export", "delete", "bulk_delete")
    action_perms = defaultdict(set, **{"bulk_delete": {"delete"}})


class CiscoDeviceTypeSupportDeleteView(generic.ObjectDeleteView):
    queryset = models.CiscoDeviceTypeSupport.objects.all()


class CiscoDeviceTypeSupportBulkDeleteView(generic.BulkDeleteView):
    queryset = models.CiscoDeviceTypeSupport.objects.all()
    # filterset = filtersets.CiscoDeviceTypeSupportFilterSet
    table = tables.CiscoDeviceTypeSupport
