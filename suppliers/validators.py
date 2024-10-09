from rest_framework.exceptions import ValidationError


def validate_product_and_prev_supplier(data):
    """Проверка: либо продукт, либо предыдущий поставщик"""
    if data.get("product") is not None and data.get("prev_supplier") is not None:
        raise ValidationError("Продукт наследуется от поставщика, при наличии поставщика поле продукта должно "
                              "быть пустым")
    elif data.get("product") is None and data.get("prev_supplier") is None:
        raise ValidationError("Выберите либо продукт, либо поставщика, от которого он будет унаследован")
    else:
        return data


def validate_debt_and_prev_supplier(data):
    """Проверка: отсутствие предыдущего поставщика не дает внести долг перед ним"""
    if data.get("prev_supplier") is None and data.get("debt") > 0:
        raise ValidationError("При отсутствии предыдущего поставщика долг перед ним внести невозможно")
    else:
        return data
