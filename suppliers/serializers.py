from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from suppliers.models import Supplier, Contacts, Product
from suppliers.service import Logger


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = "__all__"


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class SupplierSerializer(serializers.ModelSerializer):
    # validators = [HabitsDurationValidator(field="duration")]
    # validators = [HabitsDurationValidator(field="duration"), HabitsPeriodicValidator(field="periodicity")]
    logger_my = Logger("log.txt")
    logger_my(f"Time Serializer {datetime.now()}")
    contacts = ContactsSerializer(many=False)
    product = ProductsSerializer(many=False)

    class Meta:
        model = Supplier
        depth = 1
        fields = (
            "name",
            "contacts",
            "product",
            "prev_supplier",
            "debt",
            "created_at",
        )

    def create(self, validated_data):
        """Альтернативный способ сразу создать звено цепи"""
        print(f"data {self.validated_data}")

        print(type(self.validated_data["contacts"]))

        if isinstance(self.validated_data["contacts"], int):
            print(f"contacts=int!")
        else:
            print(f"{self.validated_data['contacts']}")
            contacts = self.validated_data["contacts"]
            contacts_serializer = ContactsSerializer(data=contacts)
            if contacts_serializer.is_valid():
                ct = Contacts.objects.create(**contacts)
                self.validated_data["contacts"] = ct
                # contacts_serializer.save()
            else:
                self.logger_my(f"raise ValidationError {contacts_serializer.errors} |")
                #         # print(f"raise ValidationError {contacts_serializers.errors} |")
                raise ValidationError(contacts_serializer.error_messages)

        #если есть предыдущий поставщик то сразу можно в Null ставить, создавать неиспользуемый продукт нет смысла
        if self.validated_data["prev_supplier"] != None:
            print(f"prev_supplier!")

        else:
            print(f"{self.validated_data['product']}")

            product = self.validated_data["product"]
            product_serializer = ProductsSerializer(data=product)


            if product_serializer.is_valid():
                pt = Product.objects.create(**product)
                self.validated_data["product"] = pt
            else:
                self.logger_my(f"raise ValidationError {product_serializer.errors} |")
                #         # print(f"raise ValidationError {contacts_serializers.errors} |")
                raise ValidationError(product_serializer.error_messages)
                # contacts_serializer.save()

            print(f"initial_data3 {self.validated_data} |")
            if self.is_valid():
                return Supplier.objects.create(**self.validated_data)



class SupplierSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        exclude = ("debt", "created_at")


class SupplierSerializerSimpleCreate(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = (
            "name",

            "contacts",

            "product",

            "prev_supplier",
            "debt",
            "created_at",
        )
