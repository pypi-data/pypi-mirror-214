from django import forms
from extras.forms.mixins import SavedFiltersMixin
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, FilterForm
from .models import CiscoDeviceSupport


class CiscoDeviceSupportFilterForm(SavedFiltersMixin, FilterForm):
    model = CiscoDeviceSupport

    fieldsets = (
        ("Software Release", ("recommended_release", "desired_release", "current_release",)),
        ("Device Support", ("sr_no_owner", "is_covered",)),
        ("Device Type Support", ("eox_has_error",)),
    )

    recommended_release = forms.CharField(
        required=False
    )

    desired_release = forms.CharField(
        required=False
    )

    current_release = forms.CharField(
        required=False
    )

    sr_no_owner = forms.NullBooleanField(
        required=False,
        label="Serial Owner",
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )

    is_covered = forms.NullBooleanField(
        required=False,
        label="Is Covered",
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )

    eox_has_error = forms.NullBooleanField(
        required=False,
        label="Has EoX Error",
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
