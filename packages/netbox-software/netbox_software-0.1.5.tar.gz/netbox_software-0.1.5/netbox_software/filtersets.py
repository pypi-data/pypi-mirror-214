import django_filters
from netbox.filtersets import NetBoxModelFilterSet
from .models import DeviceSoftware, VirtualMachineSoftware, SoftwareType, Vendor
from django.db.models import Q


class VendorFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Vendor
        fields = ('id', 'name',)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(comments__icontains=value)
        )


class SoftwareTypeFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = SoftwareType
        fields = ('id', 'name',)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(comments__icontains=value)
        )


class DeviceSoftwareFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = DeviceSoftware
        fields = ('id', 'name', 'software_type', 'device', 'vendor')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(version__icontains=value)
        )


class VirtualMachineSoftwareFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = VirtualMachineSoftware
        fields = ('id', 'name', 'software_type', 'virtual_machine', 'vendor')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(version__icontains=value)
        )
