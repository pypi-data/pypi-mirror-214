from django import forms
from extras.forms.mixins import SavedFiltersMixin
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, FilterForm
from utilities.forms.widgets import DatePicker
from .models import CiscoDeviceSupport


class CiscoDeviceSupportFilterForm(SavedFiltersMixin, FilterForm):
    model = CiscoDeviceSupport

    fieldsets = (
        ("General", ("model",)),
        (
            "Software Release",
            (
                "recommended_release",
                "desired_release_status",
                "desired_release",
                "current_release_status",
                "current_release",
            ),
        ),
        (
            "Device Support",
            (
                "sr_no_owner",
                "is_covered",
                "coverage_end_date__year",
            ),
        ),
        ("Device Type Support", ("eox_has_error",)),
    )

    model = forms.CharField(required=False, label="Device Type")

    recommended_release = forms.CharField(required=False, label="Recommended Release")

    desired_release_status = forms.NullBooleanField(
        required=False,
        label="Desired Release Status",
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    desired_release = forms.CharField(required=False, label="Desired Release")

    current_release_status = forms.NullBooleanField(
        required=False,
        label="Current Release Status",
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    current_release = forms.CharField(required=False, label="Current Release")

    sr_no_owner = forms.NullBooleanField(
        required=False, label="Serial Owner", widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES)
    )

    is_covered = forms.NullBooleanField(
        required=False, label="Is Covered", widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES)
    )

    coverage_end_date__year = forms.DateField(required=False, widget=DatePicker())

    eox_has_error = forms.NullBooleanField(
        required=False, label="Has EoX Error", widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES)
    )
