from django.core.exceptions import ValidationError
from django.db import models

# from suppliers.validators import validate_prev_supplier

NULLABLE = {"blank": True, "null": True}


def validate_prev_supplier(prev_supplier):
    """
    Проверяет, не вышла ли цепочка поставщиков за пределы уровней иерархической структуры
    (по ТЗ должно быть 3 уровня и не больше)
    """

    ierarchy_level = 0

    if isinstance(prev_supplier, int):
        pr_s_id = prev_supplier
    else:
        pr_s_id = prev_supplier.pk
    # pr_s_id = prev_supplier.pk

    while (pr_s_id):
        ierarchy_level += 1
        next_supplier = Supplier.objects.get(pk=pr_s_id)

        if ierarchy_level > 2:
            print(f"prev_supplier 2 {prev_supplier}")
            raise ValidationError("Длина звена цепи должен быть не больше 3 участников",
                                  params={"prev_supplier": prev_supplier})

        if next_supplier is not None:
            pr_s_id = next.prev_supplier_id

        else:
            pr_s_id = None
    else:
        # print(f"prev_supplier 3 {prev_supplier}")
        return prev_supplier

class Product(models.Model):
    product_name = models.CharField(max_length=250, verbose_name="название продукта")
    product_model = models.CharField(max_length=50, verbose_name="модель продукта")
    product_date = models.DateField(verbose_name="дата выхода продукта на рынок")

    def __str__(self):
        return f"продукт {self.product_name}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["product_name"]

class Contact(models.Model):
    email = models.EmailField(verbose_name="email")
    country = models.TextField(max_length=70, verbose_name="страна")
    city = models.TextField(max_length=70, verbose_name="город")
    street = models.TextField(max_length=150, verbose_name="улица")
    house_number = models.TextField(max_length=10, verbose_name="номер дома")

    def __str__(self):
        return f"контакт {self.email}, {self.country} {self.city} {self.street} {self.house_number}"

    class Meta:
        verbose_name = "контакт"
        verbose_name_plural = "контакты"
        ordering = ["country"]


class Supplier(models.Model):
    """Поставщик оборудования (продукта)"""

    # предприятие
    name = models.CharField(max_length=150, verbose_name="название")
    # контакты
    contacts = models.ForeignKey("Contact", on_delete=models.CASCADE, verbose_name="Контакты", **NULLABLE,
                                      validators=[validate_prev_supplier], related_name="contacts",)

    email = models.EmailField(verbose_name="email")
    country = models.TextField(max_length=70, verbose_name="страна")
    city = models.TextField(max_length=70, verbose_name="город")
    street = models.TextField(max_length=150, verbose_name="улица")
    house_number = models.TextField(max_length=10, verbose_name="номер дома")

    # продукт
    product = models.ForeignKey("Product", on_delete=models.CASCADE, verbose_name="Продукт", **NULLABLE,
                                 validators=[validate_prev_supplier], related_name="product", )


    product_name = models.CharField(max_length=250, verbose_name="название продукта")
    product_model = models.CharField(max_length=50, verbose_name="модель продукта")
    product_date = models.DateField(verbose_name="дата выхода продукта на рынок")

    # поставщик (рекурсивная связь модели)
    prev_supplier = models.ForeignKey("self", on_delete=models.CASCADE, verbose_name="Поставщик", **NULLABLE,
                                      validators=[validate_prev_supplier], related_name="prev",)
    # Задолженность перед поставщиком в денежном выражении с точностью до копеек.
    debt = models.DecimalField(max_digits=20, decimal_places=2, default=0.00,
                               verbose_name="задолженность перед поставщиком")
    # Время создания (заполняется автоматически при создании).
    created_at = models.DateTimeField(verbose_name="время создания", auto_now_add=True, )

    def __str__(self):
        return f"{self.name}, продукт {self.product_name}"

    class Meta:
        verbose_name = "поставщик"
        verbose_name_plural = "поставщики"
        ordering = ["country"]
