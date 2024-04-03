from django.urls import path
from . import views

urlpatterns = [
    path("employees/", views.get_all_employees),
    path("employees/<int:employee_id>", views.get_notifications),
    path("doctors/", views.get_all_doctors),
    path("managers/", views.get_all_managers),
    path('managers/<int:manager_id>/staff', views.get_staff),
    path('managers/<int:manager_id>/create_notification', views.create_notification),
    path('doctors/<int:doctor_id>/patients', views.get_patients),
    path('doctors/<int:doctor_id>/patients/<int:patient_id>', views.update_patient),
    path('doctors/<int:doctor_id>/forms', views.get_doctor_forms),
    path('forms/<int:form_id>', views.form_view),
    path('forms/create_form', views.new_form),
]
