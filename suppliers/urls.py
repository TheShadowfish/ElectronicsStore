from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from suppliers.apps import SuppliersConfig
from suppliers.views import SupplierViewSet, ContactsViewSet, ProductsViewSet, SupplierCreateAPIView, \
    SupplierListAPIView

router = SimpleRouter()
router.register("suppliers", SupplierViewSet, basename="suppliers")

router.register("contacts", ContactsViewSet, basename="contacts")
router.register("products", ProductsViewSet, basename="products")


app_name = SuppliersConfig.name

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),

    path("suppliers/detail_create/", SupplierCreateAPIView.as_view(),
         name="detail_create"),
    path("suppliers/detail_view/", SupplierListAPIView.as_view(),
         name="detail_view"),


]

urlpatterns += router.urls
