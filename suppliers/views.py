from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from suppliers.models import Supplier
from suppliers.permissions import IsActive
from suppliers.serializers import SupplierSerializerUpdate, SupplierSerializer


def redirect_to_admin(request):
    # Не набирать без конца адрес в браузере
    return redirect("admin/")


class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    permission_classes = (IsAuthenticated, IsActive)

    def get_serializer_class(self):
        if self.action == "update" or self.action == "partial_update":
            return SupplierSerializerUpdate
        return SupplierSerializer

    def get_queryset(self):
        """
        Фильтрация по стране в тексте запроса (?country=<countryname>),
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Supplier.objects.all()
        country = self.request.query_params.get("country")

        if country is not None:
            queryset = queryset.filter(country=country)

        return queryset
