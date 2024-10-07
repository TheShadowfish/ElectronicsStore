from datetime import datetime

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from suppliers.models import Supplier, Contacts, Product
from suppliers.service import print_console, Logger


class ContactsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contacts
        fields = "__all__"


class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"

# class SupplierCreateContaxtsMixin():
#     def create(self, validated_data):
#         import pdb; pdb.set_trace()
#
#         print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
#
#         print(f"validated_data1 {validated_data}")
#         contacts = validated_data.pop("contacts")
#         print(f"contacts {contacts}")
#
#         ct = Contacts.objects.create(**contacts)
#
#         print(f"ct {ct}")
#         print(f"validated_data2 {validated_data}")
#
#         validated_data['contacts'] = ct.pk
#
#         supplier = Supplier.objects.create(**validated_data)
#
#         return supplier



class SupplierSerializerView(serializers.ModelSerializer):
    # logger_my = Logger("log.txt")
    # logger_my("This is a test message.")

    contacts = ContactsSerializer(
        many=False, read_only=True, help_text="Контакты"
    )

    product = ProductsSerializer(
        many=False, read_only=True, help_text="Уроки, входящие в курс"
    )

    class Meta:
        model = Supplier
        # все поля модели
        fields = (
            "name",

            "contacts",

            "product",

            "prev_supplier",
            "debt",
            "created_at",
        )


class SupplierSerializer(serializers.ModelSerializer):
    # validators = [HabitsDurationValidator(field="duration")]
    # validators = [HabitsDurationValidator(field="duration"), HabitsPeriodicValidator(field="periodicity")]
    logger_my = Logger("log.txt")
    logger_my(f"Time Serializer {datetime.now()}")

    # contacts = ContactsSerializer(
    #     many=False, read_only=True, help_text="Контакты"
    # )
    #
    # product = ProductsSerializer(
    #     many=False, read_only=True, help_text="Уроки, входящие в курс"
    # )

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
        # fields = "__all__"
        # # все поля модели
        #     fields = (
        #         "name",

        #         "contacts",

        #         "product",

        #         "prev_supplier",
        #         "debt",
        #         "created_at",
        #         )
    # def get_initial(self):
    #     if isinstance(self.initial_data["contacts"], int):
    #         print(f"OK!!!")
    #     else:
    #         print(f"{self.initial_data['contacts']}")
    #
    #         self.logger_my(f"Time initial_data {datetime.now()}")
    #         self.logger_my(f"initial_data1 {self.initial_data} |")
    #         self.logger_my(f"self.initial_data['contacts'] {self.initial_data['contacts']}")
    #         contacts = self.initial_data.pop("contacts")
    #         ct = Contacts.objects.create(**contacts)
    #         self.logger_my(f"ct {ct} |")
    #         self.logger_my(f"initial_data2 {self.initial_data} |")
    #         self.data['contacts'] = ct.pk
    #         self.logger_my(f"initial_data3 {self.initial_data} |")

    def is_valid(self, raise_exception=False):
        print(f"data {self.initial_data}")


        if isinstance(self.initial_data["contacts"], int):
            print(f"OK!!!")
        else:
            print(f"{self.initial_data['contacts']}")

            self.logger_my(f"Time initial_data {datetime.now()}")
            self.logger_my(f"initial_data1 {self.initial_data} |")
            self.logger_my(f"self.initial_data['contacts'] {self.initial_data['contacts']}")
            contacts = self.initial_data.pop("contacts")
            ct = Contacts.objects.create(**contacts)
            self.logger_my(f"ct {ct} |")
            self.logger_my(f"initial_data2 {self.initial_data} |")
            self.initial_data['contacts'] = ct.pk
            self.logger_my(f"initial_data3 {self.initial_data} |")
            print(f"initial_data3 {self.initial_data} |")

            # self.is_valid()

        return super().is_valid(raise_exception=False)



            # supplier = Supplier.objects.create(**validated_data)


    # def create(self, validated_data):
    #     # код для проверки
    #
    #
    #     self.logger_my(f"validated_data1 {validated_data}")
    #
    #     self.logger_my(f"contacts {contacts} |")
    #
    #     ct = Contacts.objects.create(**contacts)
    #
    #
    #
    #
    #
    #     return supplier

class SupplierSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        exclude = ("debt", "created_at")



