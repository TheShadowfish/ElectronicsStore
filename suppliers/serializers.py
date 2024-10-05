from rest_framework import serializers

from suppliers.models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    # validators = [HabitsDurationValidator(field="duration")]
    # validators = [HabitsDurationValidator(field="duration"), HabitsPeriodicValidator(field="periodicity")]

    class Meta:
        model = Supplier
        fields = "__all__"
        # # все поля модели
        #     fields = (
        #         "name",
        #         "email",
        #         "country",
        #         "city",
        #         "street",
        #         "house_number",
        #         "product_name",
        #         "product_model",
        #         "product_date",
        #         "prev_supplier",
        #         "debt",
        #         "created_at",
        #         )


class SupplierSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        exclude = ("debt", "created_at")
