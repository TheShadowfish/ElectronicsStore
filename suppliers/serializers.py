from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from suppliers.models import Supplier, Contacts, Product
from suppliers.validators import validate_product_and_prev_supplier, validate_debt_and_prev_supplier


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = "__all__"


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class SupplierSerializer(serializers.ModelSerializer):
    validators = [serializers.UniqueTogetherValidator(fields=["name", "contacts"], queryset=Supplier.objects.all())]

    class Meta:
        model = Supplier
        # depth = 1
        fields = (
            "pk",
            "name",
            "contacts",
            "product",
            "prev_supplier",
            "debt",
            "created_at",
        )

    def create(self, validated_data):
        # Создать ссылку на продукт если есть предыдущий поставщик

        if self.validated_data.get("prev_supplier") is not None:
            # pr_s = self.validated_data.get("prev_supplier").product_id
            # print(f"{pr_s}")
            # prev = Supplier.objects.get(pk=pr_s.pk)
            # print(f"{prev}")
            product = Product.objects.get(pk=self.validated_data.get("prev_supplier").product_id)

            self.validated_data["product"] = product

        if self.is_valid():
            return Supplier.objects.create(**self.validated_data)
        else:
            # print(f"raise ValidationError {self.errors} |")

            raise ValidationError(self.error_messages)

    # def perform_create(self, serializer):
    #     supplier = serializer.save()
    #
    #
    #     if supplier.prev_supplier is not None:
    #         # pr_s = self.validated_data.get("prev_supplier").product_id
    #         # print(f"{pr_s}")
    #         # prev = Supplier.objects.get(pk=pr_s.pk)
    #         # print(f"{prev}")
    #         product = Product.objects.get(pk=self.validated_data.get("prev_supplier").product_id)
    #         #
    #         # self.validated_data["product"] = product
    #         supplier.product = Product.objects.get(pk=supplier.prev_supplier.product_id)
    #
    #     supplier.save()

    def validate(self, data):
        """
        Проверка: либо продукт, либо предыдущий поставщик validate_product_and_prev_supplier
        Проверка: отсутствие предыдущего поставщика не дает внести долг
        """

        validate_product_and_prev_supplier(data)
        validate_debt_and_prev_supplier(data)

        return data


class SupplierSerializerUpdate(serializers.ModelSerializer):
    validators = [serializers.UniqueTogetherValidator(fields=["name", "contacts"], queryset=Supplier.objects.all())]

    class Meta:
        model = Supplier
        exclude = ("prev_supplier", "debt", "created_at")

    def validate(self, data):

        validate_product_and_prev_supplier(data)
        validate_debt_and_prev_supplier(data)

        return data

    def perform_update(self, serializer):
        supplier = serializer.save()

        if supplier.prev_supplier is not None:
            supplier.product = Product.objects.get(pk=supplier.prev_supplier.product_id)

        supplier.save()


class SupplierSerializerDetail(serializers.ModelSerializer):
    contacts = ContactsSerializer(many=False)
    product = ProductsSerializer(many=False)

    class Meta:
        model = Supplier

        fields = (
            "pk",
            "name",
            "contacts",
            "product",
            "prev_supplier",
            "debt",
            "created_at",
        )

    def validate(self, data):

        validate_product_and_prev_supplier(data)
        validate_debt_and_prev_supplier(data)

        return data

    def create(self, validated_data):
        """Альтернативный способ сразу создать звено цепи"""
        # проверка контактов на валидность
        contacts = self.validated_data["contacts"]
        contacts_serializer = ContactsSerializer(data=contacts)
        if contacts_serializer.is_valid():
            ct = Contacts.objects.create(**contacts)
            self.validated_data["contacts"] = ct
        else:
            raise ValidationError(contacts_serializer.error_messages)

        if self.validated_data["prev_supplier"] is not None:
            pr_s_id = self.validated_data["prev_supplier"]
            prev = Supplier.objects.get(pk=pr_s_id)
            product = Product.objects.get(pk=prev.product_id)
            self.validated_data["product"] = product

        else:
            product = self.validated_data["product"]
            product_serializer = ProductsSerializer(data=product)

            if product_serializer.is_valid():
                pt = Product.objects.create(**product)
                self.validated_data["product"] = pt
            else:
                raise ValidationError(product_serializer.error_messages)
                # contacts_serializer.save()

        if self.is_valid():
            return Supplier.objects.create(**self.validated_data)

    def perform_create(self, serializer):
        supplier = serializer.save()

        if supplier.prev_supplier is not None:
            supplier.product = Product.objects.get(pk=supplier.prev_supplier.product_id)

        supplier.save()
