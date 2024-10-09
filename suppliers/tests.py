
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.test import APITestCase

from suppliers.models import Supplier, Product, Contacts
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
            name="testuser",
            password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.contacts = Contacts.objects.create(
            email="test@test.test",
            country = "test",
            city = "test",
            street = "test",
            house_number = "test"
        )

        self.product = Product.objects.create(
            product_name="test",
            product_model = "test",
            product_date = "2024-09-09"
        )

        self.supplier = Supplier.objects.create(
            name="название",
            contacts = self.contacts,
            product = self.product,
            prev_supplier = None,
            debt = 0,
            )




    def test_supplier_retrieve(self):
        url = reverse("suppliers:course-detail", args=(self.supplier.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.supplier.name)

    def test_supplier_create(self):
        url = reverse("suppliers:suppliers-list")
        data = {
                "name": "test",
                "contacts": self.contacts,
                "product": None,
                "prev_supplier": self.supplier,
                "debt": 100500.99
               }
        response = self.client.post(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.all().count(), 2)

    def test_supplier_update(self):
        url = reverse("suppliers:suppliers-detail", args=(self.supplier.pk,))
        data = {
            "name": "Over-test",
            "contacts": self.contacts,
            "product": None,
            "prev_supplier": self.supplier,
            "debt": 13.99
        }
        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Over-test")

    def test_course_delete(self):
        url = reverse("suppliers:suppliers-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Supplier.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("suppliers:suppliers-list")
        response = self.client.get(url)

        data = response.json()
        # print(data)

        created_text = str(self.course.created_at)
        created = created_text[0:10] + "T" + created_text[11:26] + "Z"
        updated_text = str(self.course.updated_at)
        updated = updated_text[0:10] + "T" + updated_text[11:26] + "Z"
        # print(f"created {created}")
        # print(f"updated {updated}")

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "title": self.course.title,
                    "preview": None,
                    "description": self.course.description,
                    "owner": self.user.pk,
                    "count_lessons": 1,
                    "lessons": [
                        {
                            "id": self.lesson.pk,
                            "title": self.lesson.title,
                            "description": self.lesson.description,
                            "preview": None,
                            "video_url": self.lesson.video_url,
                            "course": self.course.pk,
                            "owner": self.user.pk,
                        }
                    ],
                    "created_at": created,
                    "updated_at": updated,
                    "subscriptions": False,
                }
            ],
        }
        # print(f"created_at:{self.course.created_at} updated_at:{self.course.updated_at}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    #
    # def test_create_supplier(self):
    #     """Тестирование создания поставщика"""
    #     url = reverse("suppliers:course-list")
    #     data = {"title": "Курс 2"}
    #     response = self.client.post(url, data)
    #
    #     data = response.json()
    #
    #
    #     url = reverse("habits:habits_create")
    #     data = {
    #         "owner": self.user.pk,
    #         "place": "Магазин",
    #         "time": "18:00:00",
    #         "action": "Пойти в магазин за покупками",
    #         "duration": 60,
    #         "periodicity": 1,
    #         "sunday": True,
    #         "monday": True,
    #         "tuesday": True,
    #         "wednesday": True,
    #         "thursday": True,
    #         "friday": True,
    #         "saturday": True
    #     }
    #
    #     response = self.client.post(url, data=data)
    #     data = response.json()
    #
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(data.get("owner"), self.user.pk)
    #     self.assertEqual(data.get("place"), "Магазин")
    #     self.assertEqual(data.get("time"), "18:00:00")
    #     self.assertEqual(data.get("action"), "Пойти в магазин за покупками")
    #     self.assertEqual(data.get("duration"), 60)
    #     self.assertEqual(data.get("periodicity"), 1)
    #     self.assertEqual(data.get("friday"), True)
    #
    # def test_create_habit_duration_periodicy_validator(self):
    #     """Тестирование работы валидаиора"""
    #
    #     url = reverse("habits:habits_create")
    #     data = {
    #         "owner": self.user.pk,
    #         "place": "Магазин",
    #         "time": "18:00:00",
    #         "action": "Пойти в магазин за покупками",
    #         "duration": 180,
    #         "periodicity": 8
    #     }
    #
    #     response = self.client.post(url, data=data)
    #     data = response.json()
    #
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_create_habit_week_periodicity_validator(self):
    #     """Хотя бы один день в неделе должен быть выбран"""
    #
    #     url = reverse("habits:habits_create")
    #     data = {
    #         "owner": self.user.pk,
    #         "place": "Магазин",
    #         "time": "18:00:00",
    #         "action": "Пойти в магазин за покупками",
    #         "duration": 180,
    #         "periodicity": 8,
    #         "sunday": False,
    #         "monday": False,
    #         "tuesday": False,
    #         "wednesday": False,
    #         "thursday": False,
    #         "friday": False,
    #         "saturday": False
    #     }
    #     response = self.client.post(url, data=data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_create_habit_logic_good_habits_1(self):
    #     """Тестирование работы валидатора логики создания привычек"""
    #
    #     # У приятной привычки не может быть вознаграждения или связанной привычки.
    #
    #     url = reverse("habits:habits_create")
    #     data = {
    #         "owner": self.user.pk,
    #         "place": "Магазин",
    #         "time": "18:00:00",
    #         "action": "Пойти в магазин за покупками",
    #         "is_nice": True,
    #         "duration": 60,
    #         "periodicity": 1,
    #         "prize": "выпить коньяка"
    #     }
    #
    #     response = self.client.post(url, data=data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_create_habit_logic_good_habits_2(self):
    #     """Тестирование работы валидатора логики создания привычек"""
    #
    #     # Исключить одновременный выбор связанной привычки и указания вознаграждения.
    #
    #     url = reverse("habits:habits_create")
    #     data2 = {
    #         "owner": self.user.pk,
    #         "place": "Магазин",
    #         "time": "19:00:00",
    #         "action": "Снова пойти в магазин за покупками",
    #         "is_nice": False,
    #         "related": self.habit,
    #         "duration": 60,
    #         "periodicity": 1,
    #         "prize": "выпить еще больше коньяка"
    #     }
    #     response = self.client.post(url, data=data2)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_create_habit_logic_good_habits_3(self):
    #     """Тестирование работы валидатора логики создания привычек"""
    #
    #     # В связанные привычки могут попадать только привычки с признаком приятной привычки.
    #
    #     url = reverse("habits:habits_create")
    #
    #     data3 = {
    #         "owner": self.user.pk,
    #         "place": "Магазин",
    #         "time": "19:00:00",
    #         "action": "Снова пойти в магазин за покупками",
    #         "is_nice": False,
    #         "related": self.habit_nice_false,
    #         "duration": 60,
    #         "periodicity": 1,
    #     }
    #     response = self.client.post(url, data=data3)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # # def test_datetime_convertion(self):
    # #     updated_text = str(self.habit.updated_at)
    # #     updated = updated_text[0:10] + 'T' + updated_text[11:26] + 'Z'
    # #
    # #     print(f"{updated} | {datetime.strftime(self.habit.updated_at, '%Y-%m-%dT%H:%M:%S.%fZ')}  ")
    # #
    # #     self.assertEqual(updated, datetime.strftime(self.habit.updated_at, '%Y-%m-%dT%H:%M:%S.%fZ'))
    #
    # def test_list_habit(self):
    #     """Тестирование вывода всех привычек"""
    #
    #     url = reverse("habits:habits_list")
    #     response = self.client.get(url)
    #     data = response.json()
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(2, data.get("count"))
    #
    # def test_retrieve_habit(self):
    #     """Тестирование просмотра одной привычки"""
    #
    #     url = reverse("habits:habits_retrieve", args=(self.habit.pk,))
    #     response = self.client.get(url)
    #     data = response.json()
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data.get("owner"), self.habit.owner.id)
    #     self.assertEqual(data.get("place"), self.habit.place)
    #     self.assertEqual(data.get("time"), self.habit.time)
    #     self.assertEqual(data.get("action"), self.habit.action)
    #     self.assertEqual(data.get("duration"), self.habit.duration)
    #     self.assertEqual(data.get("periodicity"), self.habit.periodicity)
    #     self.assertEqual(data.get("friday"), True)
    #
    # def test_update_habit(self):
    #     """Тестирование изменений привычки"""
    #
    #     url = reverse("habits:habits_update", args=(self.habit.pk,))
    #     data = {
    #         "owner": self.user.pk,
    #         "place": "Фитнес-зал",
    #         "time": "19:00:00",
    #         "action": "Тренировка в фитнес-зале",
    #         "duration": 120,
    #         "periodicity": 1,
    #     }
    #     response = self.client.put(url, data)
    #     data = response.json()
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data.get("owner"), self.habit.owner.id)
    #     self.assertEqual(data.get("place"), "Фитнес-зал")
    #     self.assertEqual(data.get("time"), "19:00:00")
    #     self.assertEqual(data.get("action"), "Тренировка в фитнес-зале")
    #     self.assertEqual(data.get("duration"), 120)
    #     self.assertEqual(data.get("periodicity"), 1)
    #     self.assertEqual(data.get("is_nice"), True)
    #     self.assertEqual(data.get("sunday"), True)
    #
    # def test_delete_habit(self):
    #     """Тестирование удаления привычки"""
    #
    #     url = reverse("habits:habits_delete", args=(self.habit.pk,))
    #     response = self.client.delete(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #
    # def test_list_public_habit(self):
    #     """Тестирование вывода публичных привычек"""
    #
    #     url = reverse("habits:public_list")
    #     response = self.client.get(url)
    #     data = response.json()
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(1, data.get("count"))
