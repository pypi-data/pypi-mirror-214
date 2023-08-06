from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from .models import CiscoDeviceSupport


class CiscoDeviceSupportFilterForm(NetBoxModelFilterSetForm):
    model = CiscoDeviceSupport

    fieldsets = (
        ("SNI", ("sr_no_owner", "is_covered",)),
        ("EoX", ("eox_has_error",)),
    )

    sr_no_owner =  forms.BooleanField(
        required=False,
    )

    is_covered =  forms.BooleanField(
        required=False,
    )

    eox_has_error =  forms.BooleanField(
        required=False,
    )