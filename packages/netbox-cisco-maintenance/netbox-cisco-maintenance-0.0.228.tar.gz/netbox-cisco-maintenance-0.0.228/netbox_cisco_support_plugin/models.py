from django.db import models
from django.urls import reverse
from netbox.models import ChangeLoggedModel
from utilities.querysets import RestrictedQuerySet


class CiscoDeviceTypeSupport(ChangeLoggedModel):
    objects = RestrictedQuerySet.as_manager()

    device_type = models.OneToOneField(to="dcim.DeviceType", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.device_type}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_cisco_support_plugin:ciscodevicetypesupport_list")

    #### Fileds for CiscoDeviceTypeSupport ###################################################################

    eox_has_error = models.BooleanField(default=False, verbose_name="Has EoX Error")

    eox_error = models.CharField(max_length=100, blank=True, null=True, verbose_name="EoX Error")

    eox_announcement_date = models.DateField(blank=True, null=True, verbose_name="EoX Announcement Date")

    end_of_sale_date = models.DateField(blank=True, null=True, verbose_name="End of Sale Date")

    end_of_sw_maintenance_releases = models.DateField(
        blank=True, null=True, verbose_name="End of Sw-Maint. Date"
    )

    end_of_security_vul_support_date = models.DateField(
        blank=True, null=True, verbose_name="End of Sec-Vul. Date"
    )

    end_of_routine_failure_analysis_date = models.DateField(
        blank=True, null=True, verbose_name="End of Routine-Fail. Analysis Date"
    )

    end_of_service_contract_renewal = models.DateField(
        blank=True, null=True, verbose_name="End of Service Cont. Renewal"
    )

    last_date_of_support = models.DateField(blank=True, null=True, verbose_name="Last Date of Support")

    end_of_svc_attach_date = models.DateField(blank=True, null=True, verbose_name="End of Svc-Attach. Date")


class CiscoDeviceSupport(ChangeLoggedModel):
    objects = RestrictedQuerySet.as_manager()

    device = models.OneToOneField(to="dcim.Device", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.device}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_cisco_support_plugin:ciscodevicesupport_list")

    #### Fileds for CiscoDeviceSupport #######################################################################

    serial = models.CharField(max_length=100, blank=True, null=True, verbose_name="Serial")

    model = models.CharField(max_length=100, blank=True, null=True, verbose_name="Device Type")

    coverage_end_date = models.DateField(blank=True, null=True, verbose_name="Coverage End Date")

    service_contract_number = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Contract Number"
    )

    service_line_descr = models.CharField(max_length=100, blank=True, null=True, verbose_name="Service Level")

    warranty_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Warranty Type")

    warranty_end_date = models.DateField(blank=True, null=True, verbose_name="Warranty End Date")

    is_covered = models.BooleanField(default=False, verbose_name="Is Covered")

    sr_no_owner = models.BooleanField(default=False, verbose_name="Serial Owner")

    contract_supplier = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Contract Supplier"
    )

    api_status = models.CharField(max_length=100, blank=True, null=True, verbose_name="API Status")

    recommended_release = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Recommended Release"
    )

    desired_release = models.CharField(max_length=100, blank=True, null=True, verbose_name="Desired Release")

    current_release = models.CharField(max_length=100, blank=True, null=True, verbose_name="Current Release")

    desired_release_status = models.BooleanField(default=False, verbose_name="Desired Rel. Status")

    current_release_status = models.BooleanField(default=False, verbose_name="Current Rel. Status")

    #### Fileds same as CiscoDeviceTypeSupport ###############################################################
    # Create these fields again because referencing them from the CiscoDeviceTypeSupport model was not working

    eox_has_error = models.BooleanField(default=False, verbose_name="Has EoX Error")

    eox_error = models.CharField(max_length=100, blank=True, null=True, verbose_name="EoX Error")

    eox_announcement_date = models.DateField(blank=True, null=True, verbose_name="EoX Announcement Date")

    end_of_sale_date = models.DateField(blank=True, null=True, verbose_name="End of Sale Date")

    end_of_sw_maintenance_releases = models.DateField(
        blank=True, null=True, verbose_name="End of Sw-Maint. Date"
    )

    end_of_security_vul_support_date = models.DateField(
        blank=True, null=True, verbose_name="End of Sec-Vul. Date"
    )

    end_of_routine_failure_analysis_date = models.DateField(
        blank=True, null=True, verbose_name="End of Routine-Fail. Analysis Date"
    )

    end_of_service_contract_renewal = models.DateField(
        blank=True, null=True, verbose_name="End of Service Cont. Renewal"
    )

    last_date_of_support = models.DateField(blank=True, null=True, verbose_name="Last Date of Support")

    end_of_svc_attach_date = models.DateField(blank=True, null=True, verbose_name="End of Svc-Attach. Date")
