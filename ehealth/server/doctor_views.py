from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *
from .permissions import *


@api_view(['GET'])
@permission_classes([IsDoctorOwner])
def get_patients(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response('Doctor not found', status=status.HTTP_404_NOT_FOUND)

    patients = doctor.patients.all()
    serializer = EmployeeSerializer(patients, many=True)

    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsDoctorOwner])
def update_patient(request, doctor_id, patient_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        patient = doctor.patients.get(id=patient_id)
    except Doctor.DoesNotExist:
        return Response('Doctor not found', status=status.HTTP_404_NOT_FOUND)
    except Employee.DoesNotExist:
        return Response('Patient not found', status=status.HTTP_404_NOT_FOUND)

    if any(field not in ['med_info', 'status'] for field in request.data.keys()):
        return Response('Permission denied', status=status.HTTP_403_FORBIDDEN)

    serializer = EmployeeSerializer(patient, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsEmployeeOwner | IsDoctorOwner])
def remove_patient(request, doctor_id, employee_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        patient = doctor.patients.get(id=employee_id)
    except Doctor.DoesNotExist:
        return Response('Doctor not found', status=status.HTTP_404_NOT_FOUND)
    except Employee.DoesNotExist:
        return Response('Patient not found', status=status.HTTP_404_NOT_FOUND)

    doctor.patients.remove(patient)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsDoctorOwner])
def get_forms(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response('Doctor not found', status=status.HTTP_404_NOT_FOUND)
    forms = doctor.forms.all()
    res = [{'id': form.id, 'date': form.date.strftime(DATE_FORMAT)} for form in forms]
    return Response(res)


@api_view(['PUT'])
@permission_classes([IsDoctorOwner])
def update_doctor_code(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response('Doctor not found', status=status.HTTP_404_NOT_FOUND)

    doctor.code = random_code()
    doctor.save()
    return Response({'code': doctor.code})


@api_view(['GET'])
@permission_classes([IsEmployee])
def get_doctor_id(request, code):
    try:
        doctor = Doctor.objects.get(code=code)
    except Doctor.DoesNotExist:
        return Response('Doctor not found', status=status.HTTP_404_NOT_FOUND)

    return Response({'id': doctor.id})


@api_view(['POST'])
@permission_classes([IsDoctorOwner])
def new_form(request, doctor_id):
    request.data['doctor_id'] = doctor_id
    serializer = FormSerializer(data=request.data)
    if serializer.is_valid():
        form_instance = serializer.save()

        # questions_data = request.data.get('questions_data', [])
        # for question_data in questions_data:
        #     question_data['form_id'] = form_instance.id
        #     question_serializer = QuestionSerializer(data=question_data)
        #     if question_serializer.is_valid():
        #         question_serializer.save()
        #     else:
        #         form_instance.delete()
        #         return Response(question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsDoctorOwner])
def form_view(request, doctor_id, form_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        form = doctor.forms.get(id=form_id)
    except Doctor.DoesNotExist:
        return Response('Doctor not found', status=status.HTTP_404_NOT_FOUND)
    except Form.DoesNotExist:
        return Response('Form not found', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FormSerializer(form)
        return Response(serializer.data)

    if request.method == 'PUT':
        request.data['doctor_id'] = doctor_id
        serializer = FormSerializer(form, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        form.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
