# from django.core.exceptions import ValidationError
#
# from suppliers.models import Supplier
#
#
# def validate_prev_supplier(prev_supplier):
#     """Проверяет, не вышла ли цепочка поставщиков за пределы уровней иерархической структуры
#     (по ТЗ должно быть 3 уровня и не больше) """
#     ierarchy_level = 0
#     pr_s_id = prev_supplier
#
#     while (pr_s_id):
#         ierarchy_level += 1
#         next = Supplier.objects.get(pk=pr_s_id)
#
#         if next.prev_supplier_id is not None:
#             pr_s_id = next.prev_supplier_id
#             if ierarchy_level > 2:
#                 raise ValidationError('Длина звена цепи должен быть не больше 3 участников',
#                                         params={'prev_supplier': prev_supplier})