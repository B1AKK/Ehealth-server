from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *
from .permissions import *


@api_view(['GET'])
@permission_classes([IsManagerOwner])
def get_staff(request, manager_id):
    try:
        manager = Manager.objects.get(id=manager_id)
    except Manager.DoesNotExist:
        return Response('Manager not found', status=status.HTTP_404_NOT_FOUND)

    staff = manager.staff.all()
    serializer = EmployeeSerializer(staff, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsManager])
def create_notification(request, manager_id):
    request.data['manager_id'] = manager_id
    serializer = NotificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsManagerOwner])
def update_manager_code(request, manager_id):
    try:
        manager = Manager.objects.get(id=manager_id)
    except Manager.DoesNotExist:
        return Response('Manager not found', status=status.HTTP_404_NOT_FOUND)

    manager.code = random_code()
    manager.save()
    return Response({'code': manager.code})


@api_view(['GET'])
@permission_classes([IsEmployee])
def get_manager_id(request, code):
    try:
        manager = Manager.objects.get(code=code)
    except Manager.DoesNotExist:
        return Response('Manager not found', status=status.HTTP_404_NOT_FOUND)

    return Response({'id': manager.id})


@api_view(['GET'])
@permission_classes([IsEmployee])
def manager_info(request, manager_id):
    try:
        manager = Manager.objects.get(id=manager_id)
    except Manager.DoesNotExist:
        return Response('Manager not found', status=status.HTTP_404_NOT_FOUND)

    serializer = DoctorSerializer(manager)

    return Response(serializer.data)
