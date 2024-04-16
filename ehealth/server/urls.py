from django.urls import path
from . import views

urlpatterns = [
    path("employees/", views.get_all_employees),
    path("employees/<int:employee_id>/notifications", views.get_notifications),
    path("employees/<int:employee_id>/send_answer", views.send_answer),
    path("employees/<int:employee_id>/assign_manager/<str:code>", views.assign_manager),
    path("employees/<int:employee_id>/assign_doctor/<str:code>", views.assign_doctor),
    path("doctors/", views.get_all_doctors),
    path("doctors/<str:code>", views.get_doctor_id),
    path("doctors/<int:doctor_id>/update_code/<str:code>", views.update_doctor_code),
    path("managers/", views.get_all_managers),
    path("managers/<str:code>", views.get_manager_id),
    path('managers/<int:manager_id>/staff', views.get_staff),
    path('managers/<int:manager_id>/update_code/<str:code>', views.update_manager_code),
    path('managers/<int:manager_id>/create_notification', views.create_notification),
    path('managers/<int:manager_id>/notifications', views.get_manager_notifications),
    path('managers/<int:manager_id>/notifications/<int:notification_id>', views.update_targets),
    path('doctors/<int:doctor_id>/patients', views.get_patients),
    path('doctors/<int:doctor_id>/patients/<int:patient_id>', views.update_patient),
    path('doctors/<int:doctor_id>/forms', views.get_doctor_forms),
    path('forms/', views.forms_view),
    path('forms/<int:form_id>', views.form_view),
    path('forms/create_form', views.new_form),
]
