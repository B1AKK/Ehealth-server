from django.urls import path
from . import views

urlpatterns = [
    path("employees/", views.get_all_employees),
    path('managers/<int:manager_id>', views.get_staff),
    path('doctors/<int:doctor_id>/patients', views.get_patients),
    path('doctors/<int:doctor_id>/forms', views.get_doctor_forms),
    path('forms/<int:form_id>', views.get_form),
    path('forms/create_form', views.new_form),
]
