from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *
from .permissions import *


@api_view(['POST'])
def signup(request):
    classes = {
        'employee': EmployeeSerializer,
        'doctor': DoctorSerializer,
        'manager': ManagerSerializer
    }

    role = request.data.get('role', '')
    serializer_cls = classes.get(role, None)
    if serializer_cls is None:
        return Response('Incorrect role', status=status.HTTP_400_BAD_REQUEST)

    serializer = serializer_cls(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'role': role, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    models_cls = {
        'employee': Employee,
        'doctor': Doctor,
        'manager': Manager,
    }

    classes = {
        'employee': EmployeeSerializer,
        'doctor': DoctorSerializer,
        'manager': ManagerSerializer,
    }

    try:
        user = User.objects.get(username=request.data['username'])
        if not user.check_password(request.data['password']):
            raise User.DoesNotExist()
    except User.DoesNotExist:
        return Response('User not found', status=status.HTTP_404_NOT_FOUND)

    role = user.role
    model = models_cls.get(role, User)
    serializer_cls = classes.get(role, UserSerializer)
    user = model.objects.get(id=user.id)
    token = Token.objects.get(user=user)
    serializer = serializer_cls(user)

    return Response({'token': token.key, 'role': role, 'user': serializer.data})
