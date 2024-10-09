from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from suppliers.admin import SupplierAdmin, SupplierContacts, SupplierProduct
from suppliers.models import Supplier, Product, Contacts
from users.models import User


# from django.contrib import auth
# from auth.models import User
# auth.user

class SupplierTestCase(APITestCase):
    """Тестирование модели Supplier"""

    def setUp(self):
        """Создание тестовой модели Пользователя (с авторизацией) и поставщика"""

        # self.user = User.objects.create_user('username', 'testpassword')
        # self.assertTrue(self.client.login(username='username', password='Pas$w0rd'))
        # response = self.client.get(reverse('check_user'))
        # self.assertEqual(response.status_code, httplib.OK)

        self.user = User.objects.create(
            username="testuser",
            password="testpassword",
        )
        self.client.force_authenticate(user=self.user)

        self.contacts = Contacts.objects.create(
            email="test@test.test",
            country="test",
            city="test",
            street="test",
            house_number="test"
        )

        self.product = Product.objects.create(
            product_name="test",
            product_model="test",
            product_date="2024-09-09"
        )

        self.supplier = Supplier.objects.create(
            name="название",
            contacts=self.contacts,
            product=self.product,
            prev_supplier=None,
            debt=0,
        )

        # self.supplier_2 = Supplier.objects.create(
        #     name="название",
        #     contacts = None,
        #     product = self.product,
        #     prev_supplier = self.supplier,
        #     debt = 0,
        #     )

    def test_supplier_retrieve(self):
        url = reverse("suppliers:suppliers-detail", args=(self.supplier.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.supplier.name)

    def test_supplier_create(self):
        url = reverse("suppliers:suppliers-list")
        data = {
            "name": "test",
            "contacts": self.contacts.pk,
            "prev_supplier": self.supplier.pk,
            "debt": 100500.99
        }
        response = self.client.post(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.all().count(), 2)

    def test_supplier_create_prev_vs_product(self):
        url = reverse("suppliers:suppliers-list")
        data = {
            "name": "test",
            "contacts": self.contacts.pk,
            "product": self.product.pk,
            "prev_supplier": self.supplier.pk,
            "debt": 100500.99
        }
        response = self.client.post(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Supplier.objects.all().count(), 1)
        self.assertEqual(data, {'non_field_errors': [
            'Продукт наследуется от поставщика, при наличии поставщика поле продукта должно быть пустым']})

    def test_supplier_create_prev_null_vs_debt(self):
        url = reverse("suppliers:suppliers-list")
        data = {
            "name": "test",
            "contacts": self.contacts.pk,
            "product": self.product.pk,
            "debt": 100500.99
        }
        response = self.client.post(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Supplier.objects.all().count(), 1)
        self.assertEqual(data, {'non_field_errors': [
            'При отсутствии предыдущего поставщика долг перед ним внести невозможно']})

    def test_supplier_update(self):
        url = reverse("suppliers:suppliers-detail", args=(self.supplier.pk,))
        data = {
            "name": "Over-test",
            "contacts": self.contacts.pk,
            "product": self.product.pk,
            "prev_supplier": self.supplier.pk,
            "debt": 13.99
        }
        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Over-test")

    def test_supplier_delete(self):
        url = reverse("suppliers:suppliers-detail", args=(self.supplier.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Supplier.objects.all().count(), 0)

    def test_supplier_list(self):
        url = reverse("suppliers:suppliers-list")
        response = self.client.get(url)

        data = response.json()

        created_text = str(self.supplier.created_at)
        created = created_text[0:10] + "T" + created_text[11:26] + "Z"

        result = [
            {
                'pk': self.supplier.pk,
                'name': self.supplier.name,
                'contacts': self.supplier.contacts.pk,
                'product': self.supplier.product.pk,
                'prev_supplier': self.supplier.prev_supplier,
                'debt': '0.00',
                'created_at': created
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_suppliers_detail_view(self):
        url = reverse("suppliers:detail_view")
        response = self.client.get(url)

        data = response.json()

        created_text = str(self.supplier.created_at)
        created = created_text[0:10] + "T" + created_text[11:26] + "Z"
        result = [
            {
                'pk': self.supplier.pk,
                'name': self.supplier.name,
                'contacts':
                    {'id': self.contacts.pk,
                     'email': 'test@test.test',
                     'city': 'test',
                     'country': 'test',
                     'street': 'test',
                     'house_number': 'test'
                     },
                'product': {'id': self.product.pk,
                            'product_date': '2024-09-09',
                            'product_model': 'test',
                            'product_name': 'test'},
                'prev_supplier': self.supplier.prev_supplier,
                'debt': '0.00',
                'created_at': created
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_supplier_detail_create(self):
        url = reverse("suppliers:detail_create")

        data = {
            'name': 'self.supplier.name',
            'contacts':
                {'email': 'test@test.test',
                 'city': 'test',
                 'country': 'test',
                 'street': 'test',
                 'house_number': 'test'
                 },
            'product': {
                'product_date': '2024-09-09',
                'product_model': 'test',
                'product_name': 'test'},
            'prev_supplier': None,
            'debt': '0.00',
        }

        response = self.client.post(url, data, format="json")

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.all().count(), 2)


    def test_product_list(self):
        url = reverse("suppliers:products-list")
        response = self.client.get(url)

        # data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(data, result)

    def test_contacts_list(self):
        url = reverse("suppliers:contacts-list")
        response = self.client.get(url)

        # data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(data, result)


class AdminTestCase(APITestCase):
    """Тестирование модели Supplier"""

    def setUp(self):
        """Создание тестовой модели Пользователя (с авторизацией) и поставщика"""

        # self.user = User.objects.create_user('username', 'testpassword')
        # self.assertTrue(self.client.login(username='username', password='Pas$w0rd'))
        # response = self.client.get(reverse('check_user'))
        # self.assertEqual(response.status_code, httplib.OK)

        self.user = User.objects.create(
            username="testuser",
            password="testpassword",
        )
        self.client.force_authenticate(user=self.user)

        self.contacts = Contacts.objects.create(
            email="test@test.test",
            country="test",
            city="test",
            street="test",
            house_number="test"
        )

        self.product = Product.objects.create(
            product_name="test",
            product_model="test",
            product_date="2024-09-09"
        )

        self.supplier = Supplier.objects.create(
            name="название",
            contacts=self.contacts,
            product=self.product,
            prev_supplier=None,
            debt=0,
        )

        self.supplier_2 = Supplier.objects.create(
            name="название2",
            contacts = self.contacts,
            product = None,
            prev_supplier = self.supplier,
            debt = 0,
            )

        self.supplier_3= Supplier.objects.create(
            name="название3",
            contacts = self.contacts,
            product = None,
            prev_supplier = self.supplier_2,
            debt = 0,
            )


    def test_prev_supplier_link(self):
        obj = self.supplier_3
        link = SupplierAdmin.prev_supplier_link(self, obj)

        link_str = f'<a href="/admin/suppliers/supplier/{self.supplier_2.pk}/change/">{self.supplier_2}</a>'\

        obj = self.supplier
        link_none = SupplierAdmin.prev_supplier_link(self, obj)

        self.assertEqual(link_str, link)
        self.assertEqual(None, link_none)

    def test_ierarchy_level(self):
        lev1 = SupplierAdmin.ierarchy_level(self, self.supplier)
        lev2 = SupplierAdmin.ierarchy_level(self, self.supplier_2)
        lev3 = SupplierAdmin.ierarchy_level(self, self.supplier_3)

        self.assertEqual(lev1, "0 (first level)")
        self.assertEqual(lev2, "1 (second level)")
        self.assertEqual(lev3, "2 (third level)")


    def test_suppliers_contacts_number(self):
        number = SupplierContacts.suppliers_number(self, self.contacts)
        self.assertEqual(number, '3')

    def test_suppliers_product_number(self):
        number = SupplierProduct.suppliers_number(self, self.product)
        self.assertEqual(number, '1')

    def test_supplier_city(self):
        city = SupplierAdmin.supplier_city(self, self.supplier)
        self.assertEqual(city, "test")


# class SupplierModelsTestCase(APITestCase):
#     """Тестирование модели Supplier"""
