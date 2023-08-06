import django_tables2 as tables
from django.utils.translation import gettext as _

from netbox.tables import NetBoxTable, columns
from .models import CiscoDeviceSupport, CiscoDeviceTypeSupport


class CiscoDeviceSupportTable(NetBoxTable):
    id = tables.Column(linkify=True)

    device = tables.Column(linkify=True)

    recommended_release = columns.ContentTypeColumn(verbose_name=_("Recommended Release"))
    desired_release = columns.ContentTypeColumn(verbose_name=_("Desired Release"))
    current_release = columns.ContentTypeColumn(verbose_name=_("Current Release"))
    api_status = columns.ContentTypeColumn(verbose_name=_("API Status"))
    contract_supplier = columns.ContentTypeColumn(verbose_name=_("Contract Supplier"))
    service_line_descr = columns.ContentTypeColumn(verbose_name=_("Service Level"))
    service_contract_number = columns.ContentTypeColumn(verbose_name=_("Contract Number"))
    warranty_type = columns.ContentTypeColumn(verbose_name=_("Warrenty Type"))
    eox_error = columns.ContentTypeColumn(verbose_name=_("EOX Error"))

    desired_release_status = columns.BooleanColumn(verbose_name=_("Desired Release Status"))
    current_release_status = columns.BooleanColumn(verbose_name=_("Current Release Status"))
    sr_no_owner = columns.BooleanColumn(verbose_name=_("Serial Owner"))
    is_covered = columns.BooleanColumn(verbose_name=_("Is Covered"))
    eox_has_error = columns.BooleanColumn(verbose_name=_("EOX Error"))

    coverage_end_date = columns.DateTimeColumn()
    warranty_end_date = columns.DateTimeColumn()
    eox_announcement_date = columns.DateTimeColumn()
    end_of_sale_date = columns.DateTimeColumn()
    end_of_sw_maintenance_releases = columns.DateTimeColumn()
    end_of_security_vul_support_date = columns.DateTimeColumn()
    end_of_routine_failure_analysis_date = columns.DateTimeColumn()
    end_of_service_contract_renewal = columns.DateTimeColumn()
    last_date_of_support = columns.DateTimeColumn()
    end_of_svc_attach_date = columns.DateTimeColumn()

    # actions = columns.ActionsColumn(actions=("delete"))

    class Meta(NetBoxTable.Meta):
        model = CiscoDeviceSupport
        # fmt: off
        fields = (
            "pk", "id", "device", "serial", "recommended_release", "desired_release", "current_release",
            "desired_release_status", "current_release_status", "api_status", "sr_no_owner", "is_covered",
            "contract_supplier", "coverage_end_date", "service_line_descr", "service_contract_number",
            "warranty_end_date", "warranty_type", "eox_has_error", "eox_error", "eox_announcement_date",
            "end_of_sale_date", "end_of_sw_maintenance_releases", "end_of_security_vul_support_date",
            "end_of_routine_failure_analysis_date", "end_of_service_contract_renewal",
            "last_date_of_support", "end_of_svc_attach_date", "actions",
        )
        default_columns = (
            "pk", "id", "device", "desired_release_status", "desired_release", "current_release_status",
            "current_release", "sr_no_owner", "is_covered", "contract_supplier", "coverage_end_date",
            "service_line_descr", "eox_announcement_date", "actions",
        )
        # fmt: on


class CiscoDeviceTypeSupportTable(NetBoxTable):
    device_type = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = CiscoDeviceTypeSupport
        # fmt: off
        fields = (
            "device_type", "eox_has_error", "eox_announcement_date", "end_of_sale_date",
            "end_of_sw_maintenance_releases", "end_of_security_vul_support_date",
            "end_of_routine_failure_analysis_date", "end_of_service_contract_renewal",
            "last_date_of_support", "end_of_svc_attach_date",
        )
        default_columns = (
            "device_type", "eox_has_error", "eox_error", "eox_announcement_date", "end_of_sale_date",
            "end_of_sw_maintenance_releases", "end_of_security_vul_support_date",
            "end_of_routine_failure_analysis_date", "end_of_service_contract_renewal",
            "last_date_of_support", "end_of_svc_attach_date",
        )
        # fmt: on
