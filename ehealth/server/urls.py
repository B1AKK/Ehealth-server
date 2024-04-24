from django.urls import path
from . import views, employee_views, doctor_views, manager_views


urlpatterns = [
    path('signup', views.signup),
    path('login', views.login),

    path("employees/<int:employee_id>/notifications", employee_views.get_notifications),
    path("employees/<int:employee_id>/notifications/<int:notification_id>", employee_views.remove_notification),
    path("employees/<int:employee_id>/send_answer", employee_views.send_answer),
    path("employees/<int:employee_id>/assign_manager/<str:code>", employee_views.assign_manager),
    path("employees/<int:employee_id>/assign_doctor/<str:code>", employee_views.assign_doctor),
    path("employees/<int:employee_id>/forms", employee_views.get_forms),
    path("employees/<int:employee_id>/forms/<int:form_id>", employee_views.form_view),

    path("doctors/<str:code>", doctor_views.get_doctor_id),
    path("doctors/<int:doctor_id>/update_code", doctor_views.update_doctor_code),
    path('doctors/<int:doctor_id>/patients', doctor_views.get_patients),
    path('doctors/<int:doctor_id>/patients/<int:patient_id>', doctor_views.update_patient),
    path('doctors/<int:doctor_id>/new_form', doctor_views.new_form),
    path('doctors/<int:doctor_id>/forms', doctor_views.get_forms),
    path('doctors/<int:doctor_id>/forms/<int:form_id>', doctor_views.form_view),

    path("managers/<str:code>", manager_views.get_manager_id),
    path('managers/<int:manager_id>/staff', manager_views.get_staff),
    path('managers/<int:manager_id>/update_code', manager_views.update_manager_code),
    path('managers/<int:manager_id>/create_notification', manager_views.create_notification),
]

