from django.contrib import admin

from suppliers.models import Supplier


# Register your models here.
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "producr_name", "prev_supplier", "debt", "city"]
    list_filter = ("city", "name", "product_name")
    search_fields = ("city", "name")