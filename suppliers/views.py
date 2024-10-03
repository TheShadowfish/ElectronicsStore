from django.shortcuts import redirect
from django.urls import reverse


# Create your views here.
def redirect_to_admin(request):
    # Не набирать без конца адрес в браузере
    return redirect("admin/")