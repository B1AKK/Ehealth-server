from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


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
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        patient = doctor.patients.get(id=patient_id)
    except Doctor.DoesNotExist:
        return Response('Doctor not found', status=status.HTTP_404_NOT_FOUND)
    except Employee.DoesNotExist:
        return Response('Patient not found', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        if any(field not in ['med_info', 'status'] for field in request.data.keys()):
            return Response('Permission denied', status=status.HTTP_403_FORBIDDEN)

        serializer = EmployeeSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def form_view(request, form_id):
    try:
        form = Form.objects.get(id=form_id)
    except Form.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FormSerializer(form)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = FormSerializer(form, data=request.body)

        if serializer.is_valid():
            questions_json = request.body.get('questions_data', [])
            for question_json in questions_json:
                question_json['form_id'] = form.id
                if 'id' in question_json:
                    question_id = question_json['id']
                    try:
                        question = form.questions.get(id=question_id)
                    except Question.DoesNotExist:
                        return Response(f'Question({question_id}) not found', status=status.HTTP_400_BAD_REQUEST)
                    question_serializer = QuestionSerializer(question, data=questions_json)
                else:
                    question_serializer = QuestionSerializer(data=questions_json)
                if question_serializer.is_valid():
                    question_serializer.save()
                else:
                    return Response(question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            to_delete = request.body.get('to_delete', [])
            for question_id in to_delete:
                try:
                    form.questions.get(id=question_id).delete()
                except Question.DoesNotExist:
                    return Response(f'Question({question_id}) not found', status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    if request.method == 'DELETE':
        form.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def forms_view(request):
    forms = Form.objects.all()
    res = [{'id': form.id, 'date': form.date.strftime(DATE_FORMAT)} for form in forms]
    return Response(res)


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

            questions_data = request.data.get('questions_data', [])
            for question_data in questions_data:
                question_data['form_id'] = form_instance.id
                print(question_data)
                question_serializer = QuestionSerializer(data=question_data)
                if question_serializer.is_valid():
                    question_serializer.save()
                else:
                    form_instance.delete()
                    return Response(question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_notification(request, manager_id):
    if request.method == 'POST':
        request.data['manager_id'] = manager_id
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_notifications(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    serializer = NotificationSerializer(employee.notifications, many=True)

    return Response(serializer.data)


@api_view(['PUT'])
def update_targets(request, manager_id, notification_id):
    try:
        manager = Manager.objects.get(id=notification_id)
        notification = manager.notifications.get(id=notification_id)
    except Notification.DoesNotExist:
        return Response('Notification not found', status=status.HTTP_404_NOT_FOUND)
    except Manager.DoesNotExist:
        return Response('Manager not found', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':

        notification.targets.clear()
        targets = request.data.get('targets', [])
        for employee_id in targets:
            try:
                employee = Employee.objects.get(id=employee_id)
            except Employee.DoesNotExist:
                return Response(f'Employee {employee_id} not found', status=status.HTTP_404_NOT_FOUND)
            notification.targets.add(employee)

        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_manager_notifications(request, manager_id):
    try:
        manager = Manager.objects.get(id=manager_id)
    except Manager.DoesNotExist:
        return Response('Manager not found', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NotificationSerializer(manager.notifications, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def send_answer(request, employee_id):

    if request.method == 'POST':
        for answer_json in request.data:
            answer_json['employee_id'] = employee_id
            serializer = AnswerSerializer(data=answer_json)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
        return Response(status=status.HTTP_201_CREATED)