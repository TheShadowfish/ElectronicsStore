from django.db import models

NULLABLE = {"blank": True, "null": True}


class Supplier(models.Model):
    """
    Поставщик оборудования (продукта)
    """

    # предприятие
    name = models.CharField(max_length=150, verbose_name="название")
    # контакты
    email = models.EmailField(verbose_name="email")
    country = models.TextField(max_length=70, verbose_name="контакты")
    city = models.TextField(max_length=70, verbose_name="контакты")
    street = models.TextField(max_length=150, verbose_name="контакты")
    house_number = models.TextField(max_length=10, verbose_name="номер дома")

    # продукт
    product_name = models.CharField(max_length=250, verbose_name="название продукта")
    product_model = models.CharField(max_length=50, verbose_name="модель продукта")
    product_date = models.DateField(verbose_name="дата выхода продукта на рынок")

    # поставщик (рекурсивная связь модели)
    prev_supplier = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="Поставщик", **NULLABLE)
    # Задолженность перед поставщиком в денежном выражении с точностью до копеек.
    debt = models.FloatField(verbose_name="задолженность перед поставщиком")
    # Время создания (заполняется автоматически при создании).
    created_at = models.DateTimeField(verbose_name="время создания", auto_now_add=True,)

    def __str__(self):
        return f"Имя {self.name}, продукт {self.product_name}, предыдущий поставщик {self.prev_supplier}"

    class Meta:
        verbose_name = "поставщик"
        verbose_name_plural = "поставщики"
        ordering = ["country"]