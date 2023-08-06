from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from .models import CiscoDeviceSupport


class CiscoDeviceSupportFilterForm(NetBoxModelFilterSetForm):
    model = CiscoDeviceSupport

    fieldsets = (
        ("EOX", ("eox_has_error")),
    )

    eox_has_error = forms.BooleanField(
        required=False,
    )