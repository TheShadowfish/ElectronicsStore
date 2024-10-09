from django.contrib import admin, messages
from django.urls import reverse
from django.utils.safestring import mark_safe

from django.utils.translation import ngettext

from suppliers.models import Supplier, Contacts, Product


# Register your models here.
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "product", "debt", "supplier_city", "prev_supplier_link", "ierarchy_level"]
    list_filter = ["name", "product", "contacts__city"]
    ordering = ["name", "contacts"]
    search_fields = ["name", "supplier_city"]
    actions = ["clean_debt"]

    @admin.action(description="Clean selected " + Supplier._meta.get_field("debt").verbose_name)
    def clean_debt(self, request, queryset):
        #  + " " + Supplier._meta.verbose_name_plural.title().lower()
        updated = queryset.update(debt=0)
        self.message_user(
            request,
            ngettext(
                "%d supplier debt was successfully reseted.",
                "%d suplliers debt were successfully reseted.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.display(description="город поставщика")
    def supplier_city(self, obj):
        if obj.contacts:
            city = Contacts.objects.get(pk=obj.contacts_id).city
            return city
        else:
            return None

    @admin.display(description="ссылка на поставщика")
    def prev_supplier_link(self, obj):

        # http://127.0.0.1:8000/admin/suppliers/supplier/3/change/

        if obj.prev_supplier_id:
            my_reverse = reverse("admin:suppliers_supplier_change", args=(obj.prev_supplier_id,))
            return mark_safe(f'<a href="{my_reverse}">{obj.prev_supplier}</a>')
        else:
            return None

    @admin.display(description="уровень иерархии")
    def ierarchy_level(self, obj):
        ierarchy_level = 0
        pr_s_id = obj.prev_supplier_id

        while pr_s_id:
            ierarchy_level += 1
            next_supplier = Supplier.objects.filter(pk=pr_s_id).first()

            if next_supplier.prev_supplier_id is not None:
                pr_s_id = next_supplier.prev_supplier_id
            else:
                if ierarchy_level == 1:
                    num = "second"
                elif ierarchy_level == 2:
                    num = "third"
                else:
                    num = str(ierarchy_level + 1)
                return f"{ierarchy_level} ({num} level)"

        else:
            return f"{ierarchy_level} (first level)"


@admin.register(Contacts)
class SupplierContacts(admin.ModelAdmin):
    list_display = ["pk", "email", "country", "city", "street", "house_number", "suppliers_number"]
    list_filter = ["email", "country", "city"]
    ordering = ["country"]
    search_fields = ["country", "city", "suppliers_number"]

    @admin.display(description="число поставщиков, использующих эти контакты")
    def suppliers_number(self, obj):
        contacts_id = obj.pk

        suppliers_number = Supplier.objects.filter(contacts=contacts_id).count()

        return f"{suppliers_number}"


@admin.register(Product)
class SupplierProduct(admin.ModelAdmin):
    list_display = ["pk", "product_name", "product_model", "product_date", "suppliers_number"]
    list_filter = ["product_name", "product_model"]
    ordering = ["product_name"]
    search_fields = ["product_name"]

    @admin.display(description="число поставщиков, оперирующих продуктом")
    def suppliers_number(self, obj):
        product_id = obj.pk

        suppliers_number = Supplier.objects.filter(product=product_id).count()

        return f"{suppliers_number}"
