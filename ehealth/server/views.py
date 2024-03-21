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


def get_form(request, form_id):
    form = Form.objects.get(id=form_id)

    return JsonResponse(form.jsonify(), safe=False)


def get_doctor_forms(request, doctor_id):
    doc = Doctor.objects.get(id=doctor_id)

    res = [form.jsonify() for form in doc.forms.all()]

    return JsonResponse(res, safe=False)


@csrf_exempt
def new_form(request):
    if request.method == 'POST':
        create_form(json.loads(request.body))
        return HttpResponse("success")
