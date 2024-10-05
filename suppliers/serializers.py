from rest_framework import serializers

from suppliers.models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    # validators = [HabitsDurationValidator(field="duration")]
    # validators = [HabitsDurationValidator(field="duration"), HabitsPeriodicValidator(field="periodicity")]

    class Meta:
        model = Supplier
        fields = "__all__"

class SupplierSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = "__all__"
        exclude = ("debt",)
