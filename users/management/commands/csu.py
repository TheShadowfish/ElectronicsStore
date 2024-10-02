from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Создание суперпользователя"""

    def handle(self, *args, **options):
        user = User.objects.create(
            name="admin",
            email="admin@sky.pro",
            first_name="Admin",
            last_name="SkyPro",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

        user.set_password("1100")
        user.save()
