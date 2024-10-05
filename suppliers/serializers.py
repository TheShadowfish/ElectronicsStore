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

        # def get_queryset(self):
        #     """
        #     Optionally restricts the returned purchases to a given user,
        #     by filtering against a `username` query parameter in the URL.
        #     """
        #     queryset = Supplier.objects.all()
        #     country = self.request.query_params.get('country')
        #     print(f"country {country}")
        #     if country is not None:
        #
        #         queryset = queryset.filter(country=country)
        #         print(f"queryset = queryset.filter(country__icontains=country) {queryset}")
        #     return queryset

class SupplierSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        exclude = ("debt", "created_at")

