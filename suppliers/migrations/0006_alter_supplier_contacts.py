# Generated by Django 5.1.1 on 2024-10-07 12:00

import django.db.models.deletion
import suppliers.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("suppliers", "0005_alter_supplier_options_remove_supplier_city_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supplier",
            name="contacts",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contacts",
                to="suppliers.contacts",
                validators=[suppliers.models.validate_contacts],
                verbose_name="Контакты",
            ),
        ),
    ]
