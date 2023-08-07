from netbox.api.viewsets import NetBoxModelViewSet

from .. import models, filtersets
from .serializers import DeviceSoftwareSerializer, VirtualMachineSoftwareSerializer, SoftwareTypeSerializer, \
    VendorSerializer


class VendorViewSet(NetBoxModelViewSet):
    queryset = models.Vendor.objects.all()
    serializer_class = VendorSerializer
    filterset_class = filtersets.VendorFilterSet


class SoftwareTypeViewSet(NetBoxModelViewSet):
    queryset = models.SoftwareType.objects.all()
    serializer_class = SoftwareTypeSerializer
    filterset_class = filtersets.SoftwareTypeFilterSet


class DeviceSoftwareViewSet(NetBoxModelViewSet):
    queryset = models.DeviceSoftware.objects.prefetch_related('tags')
    serializer_class = DeviceSoftwareSerializer
    filterset_class = filtersets.DeviceSoftwareFilterSet


class VirtualMachineSoftwareViewSet(NetBoxModelViewSet):
    queryset = models.VirtualMachineSoftware.objects.prefetch_related('tags')
    serializer_class = VirtualMachineSoftwareSerializer
    filterset_class = filtersets.VirtualMachineSoftwareFilterSet
