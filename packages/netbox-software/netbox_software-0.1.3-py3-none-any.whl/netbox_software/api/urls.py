from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_software'

router = NetBoxRouter()
router.register('vendor', views.VendorViewSet)
router.register('softwaretype', views.SoftwareTypeViewSet)
router.register('device-softwares', views.DeviceSoftwareViewSet)
router.register('virtual-machine-softwares', views.VirtualMachineSoftwareViewSet)

urlpatterns = router.urls
