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
                "contract_supplier",
                "coverage_end_date",
                "service_line_descr",
            ),
        ),
        (
            "Device Type Support",
            (
                "eox_has_error",
                "eox_error",
            ),
        ),
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

    contract_supplier = forms.CharField(required=False, label="Contract Supplier")

    coverage_end_date = forms.CharField(
        required=False,
        label="Coverage End Date in Year",
        help_text="Specify the year where the coverage ends",
    )

    service_line_descr = forms.CharField(required=False, label="Service Level")

    # warranty_end_date

    eox_has_error = forms.NullBooleanField(
        required=False, label="Has EoX Error", widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES)
    )

    eox_error = forms.CharField(required=False, label="EoX Error")

    # eox_announcement_date

    # end_of_sale_date

    # end_of_sw_maintenance_releases

    # end_of_security_vul_support_date

    # end_of_routine_failure_analysis_date

    # end_of_service_contract_renewal

    # end_of_svc_attach_date

    # last_date_of_support
