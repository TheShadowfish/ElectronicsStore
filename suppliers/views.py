from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from suppliers.models import Supplier, Contacts, Product
from suppliers.permissions import IsActive
from suppliers.serializers import SupplierSerializerUpdate, SupplierSerializer, ContactsSerializer, \
    ProductsSerializer, SupplierSerializerDetail


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(operation_description="Вывод списка поставщиков"),
)
@method_decorator(
    name="create", decorator=swagger_auto_schema(operation_description="Создание нового поставщика")
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Удаление выбранного поставщика"),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(operation_description="Обновление выбранного поставщика"),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(operation_description="Обновление (частичное) выбранного поставщика"),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(operation_description="Просмотр информации о поставщиках"),
)
class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    permission_classes = (IsAuthenticated, IsActive)

    def get_serializer_class(self):
        if self.action == "update" or self.action == "partial_update":
            return SupplierSerializerUpdate
        # elif self.action == 'list':
        #     return SupplierSerializerView
        return SupplierSerializer

    def get_queryset(self):
        """Фильтрация по стране в тексте запроса (?country=<countryname>)"""

        queryset = Supplier.objects.all()
        country = self.request.query_params.get("country")

        if country is not None:
            queryset = queryset.filter(contacts__country=country)

        return queryset


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(operation_description="Вывод списка контактов"),
)
@method_decorator(
    name="create", decorator=swagger_auto_schema(operation_description="Создание нового контакта")
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Удаление выбранного контакта"),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(operation_description="Обновление выбранного контакта"),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(operation_description="Обновление (частичное) выбранного контакта"),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(operation_description="Просмотр информации о контакте"),
)
class ContactsViewSet(ModelViewSet):
    queryset = Contacts.objects.all()
    permission_classes = (IsAuthenticated, IsActive)
    serializer_class = ContactsSerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(operation_description="Вывод списка продуктов"),
)
@method_decorator(
    name="create", decorator=swagger_auto_schema(operation_description="Создание нового продукта")
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Удаление выбранного продукта"),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(operation_description="Обновление выбранного продукта"),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(operation_description="Обновление (частичное) выбранного продукта"),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(operation_description="Просмотр информации о продукте"),
)
class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated, IsActive)
    serializer_class = ProductsSerializer


class SupplierCreateAPIView(CreateAPIView):
    """Создание нового поставщика вместе с его контактами и продуктом"""

    queryset = Contacts.objects.all()
    permission_classes = (IsAuthenticated, IsActive)

    serializer_class = SupplierSerializerDetail


class SupplierListAPIView(ListAPIView):
    """Список поставщиков включая вложенные модели"""

    queryset = Contacts.objects.all()
    permission_classes = (IsAuthenticated, IsActive)
    # если возникнет необходимость показать всю цепочку поставщиков в ответе
    # тогда можно просто определить новый сериализатор с параметром в Meta depth=2
    # и вставить сюда
    serializer_class = SupplierSerializerDetail

    def get_queryset(self):
        """Фильтрация по стране в тексте запроса (?country=<countryname>)"""
        queryset = Supplier.objects.all()
        country = self.request.query_params.get("country")

        if country is not None:
            queryset = queryset.filter(contacts__country=country)

        return queryset
