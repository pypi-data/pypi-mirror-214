import django_filters
from utilities.filters import MultiValueCharFilter
from netbox.filtersets import BaseFilterSet
from .models import CiscoDeviceSupport, CiscoDeviceTypeSupport


class CiscoDeviceSupportFilterSet(BaseFilterSet):
    model = MultiValueCharFilter(lookup_expr="iexact")

    recommended_release = MultiValueCharFilter(lookup_expr="icontains")

    desired_release_status = django_filters.BooleanFilter(required=False)

    desired_release = MultiValueCharFilter(lookup_expr="iexact")

    current_release_status = django_filters.BooleanFilter(required=False)

    current_release = MultiValueCharFilter(lookup_expr="iexact")

    sr_no_owner = django_filters.BooleanFilter(required=False)

    is_covered = django_filters.BooleanFilter(required=False)

    contract_supplier = MultiValueCharFilter(lookup_expr="icontains")

    coverage_end_date = MultiValueCharFilter(lookup_expr="icontains")

    service_line_descr = MultiValueCharFilter(lookup_expr="icontains")

    warranty_end_date = MultiValueCharFilter(lookup_expr="icontains")

    eox_has_error = django_filters.BooleanFilter(required=False)

    eox_error = MultiValueCharFilter(lookup_expr="icontains")

    eox_announcement_date = MultiValueCharFilter(lookup_expr="icontains")

    end_of_sale_date = MultiValueCharFilter(lookup_expr="icontains")

    end_of_sw_maintenance_releases = MultiValueCharFilter(lookup_expr="icontains")

    end_of_security_vul_support_date = MultiValueCharFilter(lookup_expr="icontains")

    end_of_routine_failure_analysis_date = MultiValueCharFilter(lookup_expr="icontains")

    end_of_service_contract_renewal = MultiValueCharFilter(lookup_expr="icontains")

    end_of_svc_attach_date = MultiValueCharFilter(lookup_expr="icontains")

    last_date_of_support = MultiValueCharFilter(lookup_expr="icontains")

    class Meta:
        model = CiscoDeviceSupport
        # fmt: off
        fields = (
            "id", "model", "recommended_release", "desired_release_status", "desired_release",
            "current_release_status", "current_release", "sr_no_owner", "is_covered", "contract_supplier",
            "coverage_end_date", "service_line_descr", "warranty_end_date", "eox_has_error", "eox_error",
            "eox_announcement_date", "end_of_sale_date", "end_of_sw_maintenance_releases",
            "end_of_security_vul_support_date", "end_of_routine_failure_analysis_date",
            "end_of_service_contract_renewal", "end_of_svc_attach_date", "last_date_of_support"
        )
        # fmt: on


class CiscoDeviceTypeSupportFilterSet(BaseFilterSet):
    eox_has_error = django_filters.BooleanFilter(required=False)

    eox_error = MultiValueCharFilter(lookup_expr="icontains")

    eox_announcement_date = MultiValueCharFilter(lookup_expr="icontains")

    end_of_sale_date = MultiValueCharFilter(lookup_expr="icontains")

    end_of_sw_maintenance_releases = MultiValueCharFilter(lookup_expr="icontains")

    end_of_security_vul_support_date = MultiValueCharFilter(lookup_expr="icontains")

    end_of_routine_failure_analysis_date = MultiValueCharFilter(lookup_expr="icontains")

    end_of_service_contract_renewal = MultiValueCharFilter(lookup_expr="icontains")

    end_of_svc_attach_date = MultiValueCharFilter(lookup_expr="icontains")

    last_date_of_support = MultiValueCharFilter(lookup_expr="icontains")

    class Meta:
        model = CiscoDeviceTypeSupport
        # fmt: off
        fields = (
            "id", "eox_has_error", "eox_error", "eox_announcement_date", "end_of_sale_date",
            "end_of_sw_maintenance_releases", "end_of_security_vul_support_date",
            "end_of_routine_failure_analysis_date", "end_of_service_contract_renewal",
            "end_of_svc_attach_date", "last_date_of_support"
        )
        # fmt: on
