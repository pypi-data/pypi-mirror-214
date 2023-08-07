from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import DeviceSoftware, VirtualMachineSoftware, SoftwareType, Vendor
from dcim.api.nested_serializers import NestedDeviceSerializer
from virtualization.api.nested_serializers import NestedVirtualMachineSerializer


# Vendor Serializer
class VendorSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_software-api:vendor-detail')

    class Meta:
        model = Vendor
        fields = ('id', 'url', 'display', 'name', 'comments', 'custom_fields', 'created', 'last_updated',)


class NestedVendorSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_software-api:vendor-detail')

    class Meta:
        model = Vendor
        fields = ('id', 'url', 'display', 'name',)


# Vendor Serializer
class SoftwareTypeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_software-api:softwaretype-detail'
    )

    class Meta:
        model = SoftwareType
        fields = ('id', 'url', 'display', 'name', 'comments', 'custom_fields', 'created', 'last_updated',)


class NestedSoftwareTypeSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_software-api:softwaretype-detail'
    )

    class Meta:
        model = SoftwareType
        fields = ('id', 'url', 'display', 'name',)


# Device Software Serializer
class DeviceSoftwareSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_software-api:devicesoftware-detail'
    )
    device = NestedDeviceSerializer()
    software_type = NestedSoftwareTypeSerializer()
    vendor = NestedVendorSerializer()
    class Meta:
        model = DeviceSoftware
        fields = (
            'id', 'url', 'display', 'name', 'software_type', 'vendor', 'version', 'device', 'comments', 'tags',
            'custom_fields', 'created', 'last_updated',
        )


class NestedDeviceSoftwareSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_software-api:devicesoftware-detail'
    )
    class Meta:
        model = DeviceSoftware
        fields = ('id', 'url', 'display', 'name', 'version',)


# Virtual Machine Software Serializer
class VirtualMachineSoftwareSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_software-api:virtualmachinesoftware-detail'
    )

    virtual_machine = NestedVirtualMachineSerializer()
    software_type = NestedSoftwareTypeSerializer()
    vendor = NestedVendorSerializer()

    class Meta:
        model = VirtualMachineSoftware
        fields = (
            'id', 'url', 'display', 'name', 'software_type', 'vendor', 'version', 'virtual_machine', 'comments', 'tags',
            'custom_fields', 'created', 'last_updated',
        )


class NestedVirtualMachineSoftwareSerializer(WritableNestedSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_software-api:virtualmachinesoftware-detail'
    )

    class Meta:
        model = VirtualMachineSoftware
        fields = ('id', 'url', 'display', 'name', 'software_type', 'vendor', 'version',)
