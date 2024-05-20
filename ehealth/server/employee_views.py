from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *
from .permissions import *


@api_view(['GET'])
@permission_classes([IsEmployeeOwner])
def get_notifications(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return Response('Employee not found', status=status.HTTP_404_NOT_FOUND)

    serializer = NotificationSerializer(employee.notifications, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsEmployeeOwner])
def remove_notification(request, employee_id, notification_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        notification = employee.notifications.get(id=notification_id)
    except Notification.DoesNotExist:
        return Response('Notification not found', status=status.HTTP_404_NOT_FOUND)
    except Employee.DoesNotExist:
        return Response('Employee not found', status=status.HTTP_404_NOT_FOUND)

    notification.targets.remove(employee)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsEmployeeOwner])
def send_answer(request, employee_id):
    for answer_json in request.data:
        answer_json['employee_id'] = employee_id

    serializer = AnswerSerializer(data=request.data, many=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()

    return Response(status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsEmployeeOwner])
def assign_manager(request, employee_id, code):
    try:
        employee = Employee.objects.get(id=employee_id)
        manager = Manager.objects.get(code=code)
    except Employee.DoesNotExist:
        return Response('Employee not found', status=status.HTTP_404_NOT_FOUND)
    except Manager.DoesNotExist:
        return Response('Manager not found', status=status.HTTP_404_NOT_FOUND)

    employee.boss = manager
    employee.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsEmployeeOwner])
def assign_doctor(request, employee_id, code):
    try:
        employee = Employee.objects.get(id=employee_id)
        doctor = Doctor.objects.get(code=code)
    except Employee.DoesNotExist:
        return Response('Employee not found', status=status.HTTP_404_NOT_FOUND)
    except Doctor.DoesNotExist:
        return Response('Doctor not found', status=status.HTTP_404_NOT_FOUND)

    employee.assigned_doctor = doctor
    employee.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsEmployeeOwner])
def get_forms(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return Response('Employee not found', status=status.HTTP_404_NOT_FOUND)

    res = [{'id': form.id, 'date': form.date.strftime(DATE_FORMAT)} for form in employee.forms.all()]
    return Response(res)


@api_view(['GET', 'DELETE'])
@permission_classes([IsEmployeeOwner])
def form_view(request, employee_id, form_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        form = employee.forms.get(id=form_id)
    except Employee.DoesNotExist:
        return Response('Employee not found', status=status.HTTP_404_NOT_FOUND)
    except Form.DoesNotExist:
        return Response('Form not found', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FormSerializer(form)
        return Response(serializer.data)

    if request.method == 'DELETE':
        form.targets.remove(employee)
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['DELETE'])
@permission_classes([IsEmployeeOwner | IsBoss])
def remove_manager(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return Response('Employee not found', status=status.HTTP_404_NOT_FOUND)

    employee.boss = None
    employee.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsDoctorOf])
def get_answers(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return Response('Employee not found', status=status.HTTP_404_NOT_FOUND)

    forms = Form.objects.filter(questions__answers__employee=employee).distinct()
    res = [{'id': form.id, 'date': form.date.strftime(DATE_FORMAT)} for form in forms]

    return Response(res)


@api_view(['GET'])
@permission_classes([IsDoctorOf])
def get_form_answer(request, employee_id, form_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        form = Form.objects.get(id=form_id)
    except Form.DoesNotExist:
        return Response('Form not found', status=status.HTTP_404_NOT_FOUND)
    except Employee.DoesNotExist:
        return Response('Employee not found', status=status.HTTP_404_NOT_FOUND)

    answers = employee.answers.filter(question__form=form)
    serializer = AnswerSerializer(answers, many=True)

    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsEmployeeOwner | IsDoctorOf])
def remove_doctor(request, employee_id):
    try:
        patient = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return Response('Patient not found', status=status.HTTP_404_NOT_FOUND)

    patient.assigned_doctor = None
    patient.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


