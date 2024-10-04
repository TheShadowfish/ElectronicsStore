from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from suppliers.apps import SuppliersConfig
from suppliers.views import redirect_to_admin

# from habits.views import HabitsListAPIView, HabitsRetrieveAPIView, HabitsCreateAPIView, HabitsUpdateAPIView, \
#     HabitsDestroyAPIView, HabitsPublicListAPIView

app_name = SuppliersConfig.name

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),

    # path("list/", HabitsListAPIView.as_view(), name="habits_list"),
    # path("<int:pk>/", HabitsRetrieveAPIView.as_view(), name="habits_retrieve"),
    # path("create/", HabitsCreateAPIView.as_view(), name="habits_create"),
    # path("<int:pk>/update/", HabitsUpdateAPIView.as_view(), name="habits_update"),
    # path("<int:pk>/delete/", HabitsDestroyAPIView.as_view(), name="habits_delete"),
    # path("public/", HabitsPublicListAPIView.as_view(), name="public_list"),

    path("", redirect_to_admin, name="enter"),
]
