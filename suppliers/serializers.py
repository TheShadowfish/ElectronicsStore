from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from suppliers.models import Supplier, Contacts, Product
from suppliers.service import Logger
from suppliers.validators import validate_product_and_prev_supplier


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
    # logger_my = Logger("log.txt")
    # logger_my(f"Time Serializer {datetime.now()}")
    # contacts = ContactsSerializer(many=False)
    # product = ProductsSerializer(many=False)

    class Meta:
        model = Supplier
        # depth = 1
        fields = (
            "name",
            "contacts",
            "product",
            "prev_supplier",
            "debt",
            "created_at",
        )

    def create(self, validated_data):
        # Не дает одновременно заполнить продукт и поставщика"
        print("Update -> create?")

        if self.validated_data.get("product") is not None and self.validated_data.get("prev_supplier") is not None:
            raise ValidationError(f"Продукт наследуется от поставщика, при наличии поставщика поле продукта должно "
                                  f"быть пустым")
        elif self.validated_data.get("product") is None and self.validated_data.get("prev_supplier") is None:
            raise ValidationError(f"Выберите либо продукт, либо поставщика, от которого он будет унаследован")

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


    def validate(self, data):
        """
        У приятной привычки не может быть вознаграждения или связанной привычки. Исключить одновременный выбор
        связанной привычки и указания вознаграждения. В модели не должно быть заполнено одновременно и поле
        вознаграждения, и поле связанной привычки. Можно заполнить только одно из двух полей.

        Привычка должна быть исполнена не реже чем раз в 7 дней.
        """

        print("Pltcm L< dfkblfbz")

        # message = validate_related_or_prize(data) + validate_related_is_nice(data)
        # message += validate_nice_navent_prize_and_related(data) + periodicy_is_often_then_once_a_week(data)
        #
        # if message:
        raise serializers.ValidationError("Pltcm L< dfkblfbz")

        return data

    # def update(self, instance, validated_data):
    #     self.check_product_and_prev_supplier()
    #
    #
    #
    # def check_product_and_prev_supplier(self):
    #     # Не дает одновременно заполнить продукт и поставщика"
    #     print("Update -> create?")
    #
    #     if self.validated_data.get("product") is not None and self.validated_data.get("prev_supplier") is not None:
    #         raise ValidationError(f"Продукт наследуется от поставщика, при наличии поставщика поле продукта должно "
    #                               f"быть пустым")
    #     elif self.validated_data.get("product") is None and self.validated_data.get("prev_supplier") is None:
    #         raise ValidationError(f"Выберите либо продукт, либо поставщика, от которого он будет унаследован")
    #
    #     if self.validated_data.get("prev_supplier") is not None:
    #         # pr_s = self.validated_data.get("prev_supplier").product_id
    #         # print(f"{pr_s}")
    #         # prev = Supplier.objects.get(pk=pr_s.pk)
    #         # print(f"{prev}")
    #         product = Product.objects.get(pk=self.validated_data.get("prev_supplier").product_id)
    #
    #         self.validated_data["product"] = product
    #
    #     if self.is_valid():
    #         return Supplier.objects.update(**self.validated_data)
    #     else:
    #         raise ValidationError(self.error_messages)

    # def create(self, validated_data):
    #
    # def create(self, validated_data):
    #     """Альтернативный способ сразу создать звено цепи"""
    #     print(f"data {self.validated_data}")
    #
    #     print(type(self.validated_data["contacts"]))
    #
    #     if isinstance(self.validated_data["contacts"], int):
    #         print(f"contacts=int!")
    #     else:
    #         print(f"{self.validated_data['contacts']}")
    #         contacts = self.validated_data["contacts"]
    #         contacts_serializer = ContactsSerializer(data=contacts)
    #         if contacts_serializer.is_valid():
    #             ct = Contacts.objects.create(**contacts)
    #             self.validated_data["contacts"] = ct
    #             # contacts_serializer.save()
    #         else:
    #             self.logger_my(f"raise ValidationError {contacts_serializer.errors} |")
    #             #         # print(f"raise ValidationError {contacts_serializers.errors} |")
    #             raise ValidationError(contacts_serializer.error_messages)
    #
    #     #если есть предыдущий поставщик то сразу можно в Null ставить, создавать неиспользуемый продукт нет смысла
    #     if self.validated_data["prev_supplier"] != None:
    #         print(f"prev_supplier!")
    #
    #     else:
    #         print(f"{self.validated_data['product']}")
    #
    #         product = self.validated_data["product"]
    #         product_serializer = ProductsSerializer(data=product)
    #
    #
    #         if product_serializer.is_valid():
    #             pt = Product.objects.create(**product)
    #             self.validated_data["product"] = pt
    #         else:
    #             self.logger_my(f"raise ValidationError {product_serializer.errors} |")
    #             #         # print(f"raise ValidationError {contacts_serializers.errors} |")
    #             raise ValidationError(product_serializer.error_messages)
    #             # contacts_serializer.save()
    #
    #         print(f"initial_data3 {self.validated_data} |")
    #         if self.is_valid():
    #             return Supplier.objects.create(**self.validated_data)


class SupplierSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        exclude = ("debt", "created_at")

    def validate(self, data):
        return validate_product_and_prev_supplier(data)
    #     """
    #     У приятной привычки не может быть вознаграждения или связанной привычки. Исключить одновременный выбор
    #     связанной привычки и указания вознаграждения. В модели не должно быть заполнено одновременно и поле
    #     вознаграждения, и поле связанной привычки. Можно заполнить только одно из двух полей.
    #
    #     Привычка должна быть исполнена не реже чем раз в 7 дней.
    #     """
    #
    #     if self.validated_data.get("product") is not None and self.validated_data.get("prev_supplier") is not None:
    #         raise ValidationError(f"Продукт наследуется от поставщика, при наличии поставщика поле продукта должно "
    #                                   f"быть пустым")
    #     elif self.validated_data.get("product") is None and self.validated_data.get("prev_supplier") is None:
    #         raise ValidationError(f"Выберите либо продукт, либо поставщика, от которого он будет унаследован")
    #     else:
    #         return data

        # if self.validated_data.get("prev_supplier") is not None:
        #         # pr_s = self.validated_data.get("prev_supplier").product_id
        #         # print(f"{pr_s}")
        #         # prev = Supplier.objects.get(pk=pr_s.pk)
        #         # print(f"{prev}")
        #     product = Product.objects.get(pk=self.validated_data.get("prev_supplier").product_id)
        #
        #     self.validated_data["product"] = product
        #
        # if self.is_valid():
        #     return Supplier.objects.update(**self.validated_data)
        # else:
        #     raise ValidationError(self.error_messages)

        # return data

    def update(self, instance, validated_data):
        print(f'def update(self, instance, validated_data) {validated_data}')
        if self.validated_data.get("prev_supplier") is not None:
            print(f'self.validated_data.get("prev_supplier") {self.validated_data.get("prev_supplier")}')
                # pr_s = self.validated_data.get("prev_supplier").product_id
                # print(f"{pr_s}")
                # prev = Supplier.objects.get(pk=pr_s.pk)
                # print(f"{prev}")
            product = Product.objects.get(pk=self.validated_data.get("prev_supplier").product_id)
            print(f'product{product}')

            self.validated_data["product"] = product

        if self.is_valid():
            return Supplier.objects.create(**self.validated_data)
        else:
            raise ValidationError(self.error_messages)

    # def perform_update(self, serializer):
    #     supplier = serializer.save()
    #     supplier.save()

        # zone = pytz.timezone(settings.TIME_ZONE)
        # current_datetime_4_hours_ago = datetime.now(zone) - timedelta(hours=4)
        #
        # # course = get_object_or_404(Course, course.pk)
        #
        # if course.updated_at < current_datetime_4_hours_ago:
        #     send_information_about_course_update.delay(course.pk)
    #     self.check_product_and_prev_supplier()
    #
    #
    #
    # def check_product_and_prev_supplier(self):
    #     # Не дает одновременно заполнить продукт и поставщика"
    #     print("Update -> create?")
    #
    #     if self.validated_data.get("product") is not None and self.validated_data.get("prev_supplier") is not None:
    #         raise ValidationError(f"Продукт наследуется от поставщика, при наличии поставщика поле продукта должно "
    #                               f"быть пустым")
    #     elif self.validated_data.get("product") is None and self.validated_data.get("prev_supplier") is None:
    #         raise ValidationError(f"Выберите либо продукт, либо поставщика, от которого он будет унаследован")
    #
    #     if self.validated_data.get("prev_supplier") is not None:
    #         # pr_s = self.validated_data.get("prev_supplier").product_id
    #         # print(f"{pr_s}")
    #         # prev = Supplier.objects.get(pk=pr_s.pk)
    #         # print(f"{prev}")
    #         product = Product.objects.get(pk=self.validated_data.get("prev_supplier").product_id)
    #
    #         self.validated_data["product"] = product
    #
    #     if self.is_valid():
    #         return Supplier.objects.update(**self.validated_data)
    #     else:
    #         raise ValidationError(self.error_messages)

    # def create(self, validated_data):
    #
    # def create(self, validated_data):
    #     """Альтернативный способ сразу создать звено цепи"""
    #     print(f"data {self.validated_data}")
    #
    #     print(type(self.validated_data["contacts"]))
    #
    #     if isinstance(self.validated_data["contacts"], int):
    #         print(f"contacts=int!")
    #     else:
    #         print(f"{self.validated_data['contacts']}")
    #         contacts = self.validated_data["contacts"]
    #         contacts_serializer = ContactsSerializer(data=contacts)
    #         if contacts_serializer.is_valid():
    #             ct = Contacts.objects.create(**contacts)
    #             self.validated_data["contacts"] = ct
    #             # contacts_serializer.save()
    #         else:
    #             self.logger_my(f"raise ValidationError {contacts_serializer.errors} |")
    #             #         # print(f"raise ValidationError {contacts_serializers.errors} |")
    #             raise ValidationError(contacts_serializer.error_messages)
    #
    #     #если есть предыдущий поставщик то сразу можно в Null ставить, создавать неиспользуемый продукт нет смысла
    #     if self.validated_data["prev_supplier"] != None:
    #         print(f"prev_supplier!")
    #
    #     else:
    #         print(f"{self.validated_data['product']}")
    #
    #         product = self.validated_data["product"]
    #         product_serializer = ProductsSerializer(data=product)
    #
    #
    #         if product_serializer.is_valid():
    #             pt = Product.objects.create(**product)
    #             self.validated_data["product"] = pt
    #         else:
    #             self.logger_my(f"raise ValidationError {product_serializer.errors} |")
    #             #         # print(f"raise ValidationError {contacts_serializers.errors} |")
    #             raise ValidationError(product_serializer.error_messages)
    #             # contacts_serializer.save()
    #
    #         print(f"initial_data3 {self.validated_data} |")
    #         if self.is_valid():
    #             return Supplier.objects.create(**self.validated_data)



# class SupplierSerializerSimpleCreate(serializers.ModelSerializer):
#     class Meta:
#         model = Supplier
#         fields = (
#             "name",
#
#             "contacts",
#
#             "product",
#
#             "prev_supplier",
#             "debt",
#             "created_at",
#         )


class SupplierSerializerDetail(serializers.ModelSerializer):
    contacts = ContactsSerializer(many=False)
    product = ProductsSerializer(many=False)

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

    def create(self, validated_data):
        """Альтернативный способ сразу создать звено цепи"""
        print(f"data {self.validated_data}")
        print(type(self.validated_data["contacts"]))
        print(f"{self.validated_data['contacts']}")

        # проверка контактов на валидность
        contacts = self.validated_data["contacts"]
        contacts_serializer = ContactsSerializer(data=contacts)
        if contacts_serializer.is_valid():
            ct = Contacts.objects.create(**contacts)
            self.validated_data["contacts"] = ct
        else:
            print(f"raise ValidationError {contacts_serializer.errors} |")

            raise ValidationError(contacts_serializer.error_messages)

        if self.validated_data["product"] is not None and self.validated_data["prev_supplier"] is not None:
            raise ValidationError(
                f"Продукт наследуется от поставщика, при наличии поставщика поле продукта должно быть пустым",
                params={"product": self.validated_data["product"],
                        "prev_supplier": self.validated_data["prev_supplier"]})

        elif self.validated_data["product"] is None and self.validated_data["prev_supplier"] is None:
            raise ValidationError(f"Выберите либо продукт, либо поставщика, от которого он будет унаследован",
                                  params={"product": self.validated_data["product"],
                                          "prev_supplier": self.validated_data["prev_supplier"]})

        if self.validated_data["prev_supplier"] is not None:
            pr_s_id = self.validated_data["prev_supplier"]
            prev = Supplier.objects.get(pk=pr_s_id)
            product = Product.objects.get(pk=prev.product_id)
            self.validated_data["product"] = product

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
