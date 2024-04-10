from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
import json
from datetime import datetime


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


@api_view(['GET'])
def get_all_employees(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_managers(request):
    managers = Manager.objects.all()
    serializer = ManagerSerializer(managers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_doctors(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_staff(request, manager_id):
    manager = Manager.objects.get(id=manager_id)
    staff = manager.staff.all()

    serializer = EmployeeSerializer(staff, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def get_patients(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    patients = doctor.patients.all()

    serializer = EmployeeSerializer(patients, many=True)

    return Response(serializer.data)


@api_view(['PUT'])
def update_patient(request, doctor_id, patient_id):
    if request.method == 'PUT':
        doctor = Doctor.objects.get(id=doctor_id)
        patient = doctor.patients.get(id=patient_id)
        serializer = EmployeeSerializer(patient, data=request.data)
        serializer.save()
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
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


@api_view(['GET'])
def forms(request):
    forms = Form.objects.all()
    res = [{'id': form.id, 'date': form.date.strftime(DATE_FORMAT)} for form in forms]
    return Response(res)


# def send_answer(request, employee_id)


@api_view(['GET'])
def get_doctor_forms(request, doctor_id):
    doc = Doctor.objects.get(id=doctor_id)
    forms = doc.forms.all()
    serializer = FormSerializer(forms, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def new_form(request):
    if request.method == 'POST':
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            form_instance = serializer.save()

            questions_data = request.data.get('questions', [])
            for question_data in questions_data:
                question_data['form_id'] = form_instance.id
                question_serializer = QuestionSerializer(data=question_data)
                if question_serializer.is_valid():
                    question_serializer.save()
                else:
                    form_instance.delete()
                    return Response(question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    return JsonResponse(res)


def remove_target(request, employee_id, notification_id):
    if request.method == 'DELETE':
        notification = Notification.objects.get(id=notification_id)
        employee = Employee.objects.get(id=employee_id)

        notification.targets.remove(employee)