from rest_framework.exceptions import ValidationError


def validate_product_and_prev_supplier(data):

    if data.get("product") is not None and data.get("prev_supplier") is not None:
        raise ValidationError(f"Продукт наследуется от поставщика, при наличии поставщика поле продукта должно "
                          f"быть пустым")
    elif data.get("product") is None and data.get("prev_supplier") is None:
        raise ValidationError(f"Выберите либо продукт, либо поставщика, от которого он будет унаследован")
    else:

        print(f'{data.get("product")}, {data.get("prev_supplier")}')

        return data
