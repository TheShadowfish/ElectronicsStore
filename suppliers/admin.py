from django.contrib import admin, messages
from django.urls import reverse
from django.utils.safestring import mark_safe

from django.utils.translation import ngettext

from suppliers.models import Supplier


# Register your models here.
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "product_name", "debt", "city", "prev_supplier_link", "ierarchy_level"]
    list_filter = ["city", "name", "product_name"]
    ordering = ["name"]
    search_fields = ["city", "name"]
    actions = ["clean_debt"]

    # readonly_fields = ("ierarchy_level", "prev_supplier_link",)

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
            next_supplier = Supplier.objects.get(pk=pr_s_id)

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
