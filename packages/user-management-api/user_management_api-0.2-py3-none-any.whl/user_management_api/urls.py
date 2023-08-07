from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('groups', views.GroupViewSet, basename='groups')
router.register('permissions', views.PermissionViewSet, basename='permissions')
router.register('is_authenticated', views.IsAuthenticatedViewSet, basename='is_authenticated')

urlpatterns = router.urls
