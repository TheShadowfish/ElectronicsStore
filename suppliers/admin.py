from django.contrib import admin, messages

from django.utils.translation import ngettext

from suppliers.models import Supplier






# class ArticleAdmin(admin.ModelAdmin):
#     list_display = ["title", "status"]
#     ordering = ["title"]
#     actions = [make_published]
#
#
# admin.site.register(Article, ArticleAdmin)


# Register your models here.
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "product_name", "prev_supplier", "debt", "city"]
    list_filter = ["city", "name", "product_name"]
    ordering = ["name"]
    search_fields = ["city", "name"]
    actions = ["clean_debt"]

    @admin.action(description="Clean selected " + Supplier._meta.get_field('debt').verbose_name)
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