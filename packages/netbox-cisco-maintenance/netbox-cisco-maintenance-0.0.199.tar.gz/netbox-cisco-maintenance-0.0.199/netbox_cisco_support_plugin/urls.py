from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from . import models, views


urlpatterns = (
    # Cisco Device Support
    path("device-support/", views.CiscoDeviceSupportListView.as_view(), name="ciscodevicesupport_list"),
    path("device-support/delete/", views.CiscoDeviceSupportBulkDeleteView.as_view(), name="ciscodevicesupport_bulk_delete"),
    path("device-support/<int:pk>/delete/", views.CiscoDeviceSupportDeleteView.as_view(), name="ciscodevicesupport_delete"),

    # Cisco Device Type Support
    path("device-type-support/", views.CiscoDeviceTypeSupportListView.as_view(), name="ciscodevicetypesupport_list"),
)
