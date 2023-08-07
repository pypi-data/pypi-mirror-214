from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from dcim.models import Device
from virtualization.models import VirtualMachine
from .models import DeviceSoftware, VirtualMachineSoftware, SoftwareType, Vendor

from django.conf import settings
from packaging import version

NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)
if NETBOX_CURRENT_VERSION >= version.parse("3.5"):
    from utilities.forms.fields import TagFilterField, CommentField, DynamicModelChoiceField
else:
    from utilities.forms import TagFilterField, CommentField, DynamicModelChoiceField


# Vendor Form & Filter Form
class VendorForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = Vendor
        fields = ('name', 'comments',)


class VendorFilterForm(NetBoxModelFilterSetForm):
    model = Vendor
    name = forms.CharField(
        label='Название',
        required=False
    )


# SoftwareType Form & Filter Form
class SoftwareTypeForm(NetBoxModelForm):
    comments = CommentField()
    class Meta:
        model = SoftwareType
        fields = ('name', 'comments',)


class SoftwareTypeFilterForm(NetBoxModelFilterSetForm):
    model = SoftwareType
    name = forms.CharField(
        label='Название',
        required=False
    )

# Device Software Form & Filter Form
class DeviceSoftwareForm(NetBoxModelForm):
    comments = CommentField()

    device = DynamicModelChoiceField(
        label='Устройство',
        queryset=Device.objects.all()
    )
    software_type = DynamicModelChoiceField(
        label='Тип',
        queryset=SoftwareType.objects.all()
    )
    vendor = DynamicModelChoiceField(
        label='Разработчик',
        queryset=Vendor.objects.all()
    )

    class Meta:
        model = DeviceSoftware
        fields = ('name', 'software_type', 'device', 'vendor', 'version', 'comments', 'tags')


class DeviceSoftwareFilterForm(NetBoxModelFilterSetForm):
    model = DeviceSoftware

    name = forms.CharField(
        label='Название',
        required=False
    )

    device = forms.ModelMultipleChoiceField(
        label='Устройство',
        queryset=Device.objects.all(),
        required=False
    )
    software_type = forms.ModelMultipleChoiceField(
        label='Тип',
        queryset=SoftwareType.objects.all(),
        required=False
    )
    vendor = forms.ModelMultipleChoiceField(
        label='Разработчик',
        queryset=Vendor.objects.all(),
        required=False
    )

    tag = TagFilterField(model)


# Virtual Machine Software Form & Filter Form
class VirtualMachineSoftwareForm(NetBoxModelForm):
    comments = CommentField()

    virtual_machine = DynamicModelChoiceField(
        label='Устройство',
        queryset=VirtualMachine.objects.all()
    )
    software_type = DynamicModelChoiceField(
        label='Тип',
        queryset=SoftwareType.objects.all()
    )
    vendor = DynamicModelChoiceField(
        label='Разработчик',
        queryset=Vendor.objects.all()
    )

    class Meta:
        model = VirtualMachineSoftware
        fields = ('name', 'software_type', 'virtual_machine', 'vendor', 'version', 'comments', 'tags')


class VirtualMachineSoftwareFilterForm(NetBoxModelFilterSetForm):
    model = VirtualMachineSoftware

    name = forms.CharField(
        label='Название',
        required=False
    )

    virtual_machine = forms.ModelMultipleChoiceField(
        label='Виртуальая машина',
        queryset=VirtualMachine.objects.all(),
        required=False
    )

    software_type = forms.ModelMultipleChoiceField(
        label='Тип',
        queryset=SoftwareType.objects.all(),
        required=False
    )
    vendor = forms.ModelMultipleChoiceField(
        label='Разработчик',
        queryset=Vendor.objects.all(),
        required=False
    )

    tag = TagFilterField(model)
