from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from . import models, views


urlpatterns = (
    # Cisco Device Support
    path("device-support/", views.CiscoDeviceSupportListView.as_view(), name="ciscodevicesupport_list"),
    path("device-support/add/", views.CiscoDeviceSupportEditView.as_view(), name="ciscodevicesupport_add"),
    path("device-support/<int:pk>/edit/", views.CiscoDeviceSupportEditView.as_view(), name="ciscodevicesupport_edit"),
    path("device-support/<int:pk>/delete/", views.CiscoDeviceSupportDeleteView.as_view(), name="ciscodevicesupport_delete"),
    path(
        "device-support/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="CiscoDeviceSupport_changelog",
        kwargs={"model": models.CiscoDeviceSupport},
    ),
    # Cisco Device Type Support
    path("device-type-support/", views.CiscoDeviceTypeSupportListView.as_view(), name="ciscodevicetypesupport_list"),
    path("device-type-support/add/", views.CiscoDeviceTypeSupportEditView.as_view(), name="ciscodevicetypesupport_add"),
    path("device-type-support/<int:pk>/edit/", views.CiscoDeviceTypeSupportEditView.as_view(), name="ciscodevicetypesupport_edit"),
    path("device-type-support/<int:pk>/delete/", views.CiscoDeviceTypeSupportDeleteView.as_view(), name="ciscodevicetypesupport_delete"),
    path(
        "device-type-support/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="CiscoDeviceSupport_changelog",
        kwargs={"model": models.CiscoDeviceTypeSupport},
    ),
)
