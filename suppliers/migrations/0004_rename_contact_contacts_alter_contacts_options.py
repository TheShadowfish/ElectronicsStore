# Generated by Django 5.1.1 on 2024-10-07 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("suppliers", "0003_contact_product_supplier_contacts_supplier_product"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Contact",
            new_name="Contacts",
        ),
        migrations.AlterModelOptions(
            name="contacts",
            options={
                "ordering": ["country"],
                "verbose_name": "контакты",
                "verbose_name_plural": "контакты",
            },
        ),
    ]
