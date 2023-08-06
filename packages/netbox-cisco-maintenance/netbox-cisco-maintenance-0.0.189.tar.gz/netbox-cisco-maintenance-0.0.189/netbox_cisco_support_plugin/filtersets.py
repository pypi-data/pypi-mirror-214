from netbox.filtersets import NetBoxModelFilterSet
from .models import CiscoDeviceSupport, CiscoDeviceTypeSupport

"""
class CiscoDeviceSupportFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = CiscoDeviceSupport
        fields = [
            "id", "device", "model", "serial", "api_status", "sr_no_owner", "is_covered",
            "coverage_end_date", "contract_supplier", "service_line_descr", "service_contract_number",
            "warranty_end_date", "warranty_type", "recommended_release", "desired_release",
            "current_release", "desired_release_status", "current_release_status", "eox_has_error",
            "eox_error", "eox_announcement_date", "end_of_sale_date", "end_of_sw_maintenance_releases",
            "end_of_security_vul_support_date", "end_of_routine_failure_analysis_date",
            "end_of_service_contract_renewal", "last_date_of_support", "end_of_svc_attach_date",
        ]

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)


class CiscoDeviceTypeSupportFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = CiscoDeviceTypeSupport
        fields = [
            "id", "device_type", "eox_has_error", "eox_error", "eox_announcement_date",
            "end_of_sale_date", "end_of_sw_maintenance_releases", "end_of_security_vul_support_date",
            "end_of_routine_failure_analysis_date", "end_of_service_contract_renewal", 
            "last_date_of_support", "end_of_svc_attach_date",
        ]

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)
"""
