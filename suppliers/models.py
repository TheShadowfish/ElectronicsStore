from django.core.exceptions import ValidationError
from django.db import models


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

    while pr_s_id:
        ierarchy_level += 1
        next_supplier = Supplier.objects.filter(pk=pr_s_id).first()
        if ierarchy_level > 2:
            raise ValidationError("Длина звена цепи должен быть не больше 3 участников",
                                  params={"prev_supplier": prev_supplier})

        if next_supplier is not None:

            pr_s_id = next_supplier.prev_supplier_id

        else:
            pr_s_id = None
    else:
        return prev_supplier


class Product(models.Model):
    product_name = models.CharField(max_length=250, verbose_name="название продукта")
    product_model = models.CharField(max_length=50, verbose_name="модель продукта")
    product_date = models.DateField(verbose_name="дата выхода продукта на рынок")

    def __str__(self):
        return f"{self.product_name}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["product_name"]


class Contacts(models.Model):
    email = models.EmailField(verbose_name="email")
    country = models.TextField(max_length=70, verbose_name="страна")
    city = models.TextField(max_length=70, verbose_name="город")
    street = models.TextField(max_length=150, verbose_name="улица")
    house_number = models.TextField(max_length=10, verbose_name="номер дома")

    def __str__(self):
        return f"контакты: {self.email}, {self.country} {self.city} {self.street} {self.house_number}"

    class Meta:
        verbose_name = "контакты"
        verbose_name_plural = "контакты"
        ordering = ["country"]


class Supplier(models.Model):
    """Поставщик оборудования (продукта)"""

    # предприятие
    name = models.CharField(max_length=150, verbose_name="название")
    # контакты
    contacts = models.ForeignKey("Contacts", on_delete=models.CASCADE, verbose_name="Контакты",
                                 related_name="contacts", )

    # продукт
    product = models.ForeignKey("Product", on_delete=models.CASCADE, verbose_name="Продукт", **NULLABLE,
                                related_name="product", )

    # поставщик (рекурсивная связь модели)
    prev_supplier = models.ForeignKey("self", on_delete=models.CASCADE, verbose_name="Поставщик", **NULLABLE,
                                      validators=[validate_prev_supplier], related_name="prev", )
    # Задолженность перед поставщиком в денежном выражении с точностью до копеек.
    debt = models.DecimalField(max_digits=20, decimal_places=2, default=0.00,
                               verbose_name="задолженность перед поставщиком")
    # Время создания (заполняется автоматически при создании).
    created_at = models.DateTimeField(verbose_name="время создания", auto_now_add=True, )

    def __str__(self):
        return f"{self.name}, продукт {self.product}"

    class Meta:
        verbose_name = "поставщик"
        verbose_name_plural = "поставщики"
        ordering = ["name"]

    def clean(self):
        # Не дает одновременно заполнить продукт и поставщика
        # Не дает установить долг перед поставщиком если его нет

        if self.product is not None and self.prev_supplier is not None:
            raise ValidationError("Продукт наследуется от поставщика, при наличии поставщика поле продукта должно "
                                  "быть пустым",
                                  params={"product": self.product, "prev_supplier": self.prev_supplier})
        elif self.product is None and self.prev_supplier is None:
            raise ValidationError("Выберите либо продукт, либо поставщика, от которого он будет унаследован",
                                  params={"product": self.product, "prev_supplier": self.prev_supplier})

        if self.debt != 0 and self.prev_supplier is None:
            raise ValidationError("При отсутствии предыдущего поставщика долг перед ним внести невозможно",
                                  params={"product": self.product, "prev_supplier": self.prev_supplier})

        if self.prev_supplier is not None:
            pr_s_id = self.prev_supplier_id
            prev = Supplier.objects.get(pk=pr_s_id)
            product = Product.objects.get(pk=prev.product_id)

            self.product = product
