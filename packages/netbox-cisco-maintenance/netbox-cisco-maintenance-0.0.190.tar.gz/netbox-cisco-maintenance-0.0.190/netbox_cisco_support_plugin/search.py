from netbox.search import SearchIndex, register_search
from .models import CiscoDeviceSupport, CiscoDeviceTypeSupport

# Reindex the indexers after changing the fields -> $ ./manage.py reindex netbox_cisco_support_plugin

"""
@register_search
class CiscoDeviceSupportIndex(SearchIndex):
    model = CiscoDeviceSupport
    fields = (
        ("is_covered", 500),
        ("sr_no_owner", 500),
        ("contract_supplier", 1000),
        ("api_status", 50000),
        ("current_release", 1000),
        ("desired_release_status", 1000),
        ("current_release_status", 1000),
    )


@register_search
class CiscoDeviceTypeSupportIndex(SearchIndex):
    model = CiscoDeviceTypeSupport
    fields = (
        ("eox_has_error", 500),
        ("eox_error", 500),
    )
"""