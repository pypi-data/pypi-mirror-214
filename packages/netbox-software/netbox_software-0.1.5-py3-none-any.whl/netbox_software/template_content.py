from extras.plugins import PluginTemplateExtension
from django.conf import settings
from .models import DeviceSoftware, VirtualMachineSoftware

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_software', {})


class DeviceSoftwareList(PluginTemplateExtension):
    model = 'dcim.device'
    def left_page(self):
        if plugin_settings.get('enable_device_software') and plugin_settings.get('device_software_location') == 'left':

            return self.render('netbox_software/devicesoftware_include.html', extra_context={
                'device_software': DeviceSoftware.objects.filter(device=self.context['object']),
            })
        else:
            return ""

    def right_page(self):
        if plugin_settings.get('enable_device_software') and plugin_settings.get('device_software_location') == 'right':

            return self.render('netbox_software/devicesoftware_include.html', extra_context={
                'device_software': DeviceSoftware.objects.filter(device=self.context['object']),
            })
        else:
            return ""


class VirtualMachineSoftwareList(PluginTemplateExtension):
    model = 'virtualization.virtualmachine'

    def left_page(self):
        if plugin_settings.get('enable_virtual-machine_software') and plugin_settings.get('virtual-machine_software_location') == 'left':

            return self.render('netbox_software/virtualmachinesoftware_include.html', extra_context={
                'virtual_machine_software': VirtualMachineSoftware.objects.filter(virtual_machine=self.context['object']),
            })
        else:
            return ""

    def right_page(self):
        if plugin_settings.get('enable_virtual-machine_software') and plugin_settings.get('virtual-machine_software_location') == 'right':

            return self.render('netbox_software/virtualmachinesoftware_include.html', extra_context={
                'virtual_machine_software': VirtualMachineSoftware.objects.filter(virtual_machine=self.context['object']),
            })
        else:
            return ""


template_extensions = [DeviceSoftwareList, VirtualMachineSoftwareList]
