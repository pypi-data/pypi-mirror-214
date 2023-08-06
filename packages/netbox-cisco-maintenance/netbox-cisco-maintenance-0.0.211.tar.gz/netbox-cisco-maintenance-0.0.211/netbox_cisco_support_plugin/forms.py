from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from .models import CiscoDeviceSupport


class CiscoDeviceSupportFilterForm(NetBoxModelFilterSetForm):
    model = CiscoDeviceSupport

    fieldsets = (
        (None, ("q", "filter_id")),
    )