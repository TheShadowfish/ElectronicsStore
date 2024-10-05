from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from suppliers.models import Supplier
from suppliers.permissions import IsActive
from suppliers.serializers import SupplierSerializerUpdate, SupplierSerializer


# Create your views here.
def redirect_to_admin(request):
    # Не набирать без конца адрес в браузере
    return redirect("admin/")

class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    permission_classes = (IsAuthenticated, IsActive)

    # def perform_create(self, serializer):
    #     serializer.save(reg_user=self.request.user)

    # serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.action == "update":
            return SupplierSerializerUpdate
        return SupplierSerializer
