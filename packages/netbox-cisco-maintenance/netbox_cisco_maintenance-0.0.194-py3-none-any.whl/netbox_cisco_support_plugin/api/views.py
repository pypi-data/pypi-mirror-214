from netbox.api.viewsets import NetBoxModelViewSet

from .. import models
from .serializers import CiscoDeviceSupportSerializer, CiscoDeviceTypeSupportSerializer


class CiscoDeviceSupportViewSet(NetBoxModelViewSet):
    queryset = models.CiscoDeviceSupport.objects.all().prefetch_related("device")
    serializer_class = CiscoDeviceSupportSerializer


class CiscoDeviceTypeSupportViewSet(NetBoxModelViewSet):
    queryset = models.CiscoDeviceTypeSupport.objects.all().prefetch_related("device_type")
    serializer_class = CiscoDeviceTypeSupportSerializer
