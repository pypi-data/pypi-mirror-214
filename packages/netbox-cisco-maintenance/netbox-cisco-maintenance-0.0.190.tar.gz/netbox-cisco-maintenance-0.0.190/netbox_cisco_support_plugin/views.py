from collections import defaultdict
from netbox.views import generic
from . import filtersets, forms, models, tables


class CiscoDeviceSupportListView(generic.ObjectListView):
    actions = ("export", "bulk_delete")
    action_perms = defaultdict(set, **{"bulk_delete": {"delete"}})
    queryset = models.CiscoDeviceSupport.objects.all()
    table = tables.CiscoDeviceSupportTable
    # filterset = filtersets.CiscoDeviceSupportFilterSet
    # filterset_form = forms.CiscoDeviceSupportFilterForm

"""
class CiscoDeviceSupportView(generic.ObjectView):
    queryset = models.CiscoDeviceSupport.objects.all()


class CiscoDeviceSupportEditView(generic.ObjectEditView):
    queryset = models.CiscoDeviceSupport.objects.all()
    form = forms.CiscoDeviceSupportForm


class CiscoDeviceSupportDeleteView(generic.ObjectDeleteView):
    queryset = models.CiscoDeviceSupport.objects.all()
"""

class CiscoDeviceTypeSupportListView(generic.ObjectListView):
    actions = ("export", "bulk_delete")
    action_perms = defaultdict(set, **{"bulk_delete": {"delete"}})
    queryset = models.CiscoDeviceTypeSupport.objects.all()
    table = tables.CiscoDeviceTypeSupportTable
    # filterset = filtersets.CiscoDeviceTypeSupportFilterSet
    # filterset_form = forms.CiscoDeviceTypeSupportFilterForm

"""
class CiscoDeviceTypeSupportView(generic.ObjectView):
    queryset = models.CiscoDeviceSupport.objects.all()


class CiscoDeviceTypeSupportEditView(generic.ObjectEditView):
    queryset = models.CiscoDeviceSupport.objects.all()
    form = forms.CiscoDeviceTypeSupportForm


class CiscoDeviceTypeSupportDeleteView(generic.ObjectDeleteView):
    queryset = models.CiscoDeviceSupport.objects.all()
"""
