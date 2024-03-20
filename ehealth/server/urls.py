from django.urls import path
from . import views

urlpatterns = [
    path("employees/", views.get_all_employees),
]
