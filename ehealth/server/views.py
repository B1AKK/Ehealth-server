from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json


form_json = {
    'name': 'test',
    'description': 'this is a test form',
    'doctor_id': 4,
    'questions': [
        {
            'question_text': 'How are you today?',
            'type': 'rb',
            'options': ['good', 'bad']
        },
        {
            'question_text': 'Test',
            'type': 'txt',
            'options': []
        }
    ]
}


def get_all_employees(request):
    employees = Employee.objects.all()
    res = [employee.jsonify() for employee in employees]
    return JsonResponse(res, safe=False)


def get_all_managers(request):
    managers = Manager.objects.all()
    res = [manager.jsonify() for manager in managers]
    return JsonResponse(res, safe=False)


def get_all_doctors(request):
    doctors = Doctor.objects.all()
    res = [doctor.jsonify() for doctor in doctors]
    return JsonResponse(res, safe=False)


def get_staff(request, manager_id):
    manager = Manager.objects.get(id=manager_id)
    staff = manager.staff.all()

    res = [employee.jsonify() for employee in staff]

    return JsonResponse(res, safe=False)


def get_patients(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    patients = doctor.patients.all()

    res = [employee.jsonify() for employee in patients]

    return JsonResponse(res, safe=False)


@csrf_exempt
def update_patient(request, doctor_id, patient_id):
    if request.method == 'PUT':
        doctor = Doctor.objects.get(id=doctor_id)
        patient = doctor.patients.get(id=patient_id)
        data = json.loads(request.body)
        patient.status = data['status']
        patient.med_info = data['med_info']
        patient.save()
        return HttpResponse('success')


@csrf_exempt
def form_view(request, form_id):
    if request.method == 'GET':
        form = Form.objects.get(id=form_id)

        return JsonResponse(form.jsonify(), safe=False)

    if request.method == 'PUT':
        form_json = json.loads(request.body)
        print(form_json)
        update_form(form_json, form_id)

        return HttpResponse("success")

    if request.method == 'DELETE':
        Form.objects.get(id=form_id).delete()


def get_doctor_forms(request, doctor_id):
    doc = Doctor.objects.get(id=doctor_id)

    res = [form.jsonify() for form in doc.forms.all()]

    return JsonResponse(res, safe=False)


@csrf_exempt
def new_form(request):
    if request.method == 'POST':
        create_form(json.loads(request.body))
        return HttpResponse("success")


@csrf_exempt
def create_notification(request, manager_id):
    if request.method == 'POST':
        notification_json = json.loads(request.body)
        notification = Notification(text=notification_json['text'], manager=Manager.objects.get(id=manager_id))
        for emp_id in notification_json['targets']:
            employee = Employee.objects.get(id=emp_id)
            notification.targets.add(employee)


def get_notifications(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    res = [notification.text for notification in employee.notifications]

    return HttpResponse(res)