from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_sb_dc_accessdata'

router = NetBoxRouter()
router.register('keycard', views.KeycardViewSet)
router.register('key', views.KeyViewSet)

urlpatterns = router.urls