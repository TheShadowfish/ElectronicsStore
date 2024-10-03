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
    list_display = ["pk", "name", "product_name", "prev_supplier", "debt", "city", "prev_supplier_id", "prev_supplier_url"]
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

    def prev_supplier_url(self, obj):
        # @property
        # @admin.display(description='Предыдущий поставщик - ссылка')
        # def url(self):
        pr_s_id = obj.prev_supplier_id
        # Supplier.objects.filter(prev_supplier=self.prev_supplier)
        #
        # # http://127.0.0.1:8000/admin/suppliers/supplier/2/change/
        #
        # host2 = self.
        host = 'localhost'
            # # plural = self._meta.verbose_name_plural.title().lower()
            # # singular = self._meta.verbose_name.title().lower()
            # # Supplier._meta.verbose_name_plural.title().lower()
            # # url =  f"http://{host}/admin/{'suppliers'}/{'supplier'}/{}/change/"
            # return f"http://{host}/admin/{'suppliers'}/{'supplier'}/{pr_s_id.pk}/change/"
            #
        if(pr_s_id):
            # print(f"http://{host}/admin/{'suppliers'}/{'supplier'}/{pr_s_id.pk}/change/")
            return f"http://{host}/admin/{'suppliers'}/{'supplier'}/{pr_s_id}/change/"
                # return "Здесь Должна Быть Ссылка (в Сибирь)"
        else:
            return None

