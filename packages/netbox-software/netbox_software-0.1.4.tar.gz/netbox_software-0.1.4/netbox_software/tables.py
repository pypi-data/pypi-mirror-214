import django_tables2 as tables

from netbox.tables import NetBoxTable, columns
from .models import DeviceSoftware, VirtualMachineSoftware, Vendor, SoftwareType

SOFTWARE_TYPE_SOFTWARE_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_software:softwaretype' pk=record.pk %}">{% firstof record.name record.name %}</a>
{% endif %}
"""

VENDOR_SOFTWARE_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_software:vendor' pk=record.pk %}">{% firstof record.name record.name %}</a>
{% endif %}
"""

DEVICE_SOFTWARE_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_software:devicesoftware' pk=record.pk %}">{% firstof record.name record.name %}</a>
{% endif %}
"""

VIRTUAL_MACHINE_SOFTWARE_LINK = """
{% if record %}
    <a href="{% url 'plugins:netbox_software:virtualmachinesoftware' pk=record.pk %}">
    {% firstof record.name record.name %}</a>
{% endif %}
"""


class VendorTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=VENDOR_SOFTWARE_LINK)

    class Meta(NetBoxTable.Meta):
        model = Vendor
        fields = ('pk', 'id', 'name', 'comments', 'actions', 'created', 'last_updated',)
        default_columns = ('name',)


class SoftwareTypeTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=SOFTWARE_TYPE_SOFTWARE_LINK)

    class Meta(NetBoxTable.Meta):
        model = SoftwareType
        fields = ('pk', 'id', 'name', 'comments', 'actions', 'created', 'last_updated',)
        default_columns = ('name',)


class DeviceSoftwareTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=DEVICE_SOFTWARE_LINK)
    software_type = tables.Column(
        linkify=True
    )
    vendor = tables.Column(
        linkify=True
    )
    device = tables.Column(
        linkify=True
    )

    tags = columns.TagColumn(
        url_name='dcim:sitegroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = DeviceSoftware
        fields = ('pk', 'id', 'name', 'software_type', 'vendor', 'version', 'device', 'comments', 'actions',
                  'created', 'last_updated', 'tags')
        default_columns = ('name', 'software_type', 'device', 'tags')


class VirtualMachineSoftwareTable(NetBoxTable):
    name = tables.TemplateColumn(template_code=VIRTUAL_MACHINE_SOFTWARE_LINK)
    software_type = tables.Column(
        linkify=True
    )
    vendor = tables.Column(
        linkify=True
    )
    virtual_machine = tables.Column(
        linkify=True
    )

    tags = columns.TagColumn(
        url_name='dcim:sitegroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = VirtualMachineSoftware
        fields = ('pk', 'id', 'name', 'software_type', 'vendor', 'version', 'virtual_machine', 'comments', 'actions',
                  'created', 'last_updated', 'tags')
        default_columns = ('name', 'software_type', 'virtual_machine', 'tags')
