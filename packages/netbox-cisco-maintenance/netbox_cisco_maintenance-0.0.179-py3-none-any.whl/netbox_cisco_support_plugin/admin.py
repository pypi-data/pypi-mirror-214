from django.contrib import admin
from .models import CiscoDeviceTypeSupport, CiscoDeviceSupport


@admin.register(CiscoDeviceTypeSupport)
class CiscoSupportAdmin(admin.ModelAdmin):
    list_display = (
        "device_type",
        "eox_has_error",
        "eox_error",
        "eox_announcement_date",
        "end_of_sale_date",
        "end_of_sw_maintenance_releases",
        "end_of_security_vul_support_date",
        "end_of_routine_failure_analysis_date",
        "end_of_service_contract_renewal",
        "last_date_of_support",
        "end_of_svc_attach_date",
    )


@admin.register(CiscoDeviceSupport)
class CiscoSupportAdmin(admin.ModelAdmin):
    list_display = (
        "device",
        "serial",
        "api_status",
        "recommended_release",
        "desired_release",
        "current_release",
        "desired_release_status",
        "current_release_status",
        "contract_supplier",
        "sr_no_owner",
        "is_covered",
        "service_contract_number",
        "service_line_descr",
        "model",
        "coverage_end_date",
        "warranty_end_date",
        "warranty_type",
        "eox_has_error",
        "eox_error",
        "eox_announcement_date",
        "end_of_sale_date",
        "end_of_sw_maintenance_releases",
        "end_of_security_vul_support_date",
        "end_of_routine_failure_analysis_date",
        "end_of_service_contract_renewal",
        "last_date_of_support",
        "end_of_svc_attach_date",
    )
