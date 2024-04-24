from rest_framework.permissions import BasePermission
from .models import *


class IsDoctorOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.id == view.kwargs.get('doctor_id', 0) and \
            request.user.is_authenticated


class IsManagerOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.id == view.kwargs.get('manager_id', 0) and \
            request.user.is_authenticated


class IsEmployeeOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.id == view.kwargs.get('employee_id', 0) and \
            request.user.is_authenticated


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return Doctor.objects.filter(id=request.user.id).exists() and \
            request.user.is_authenticated


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return Employee.objects.filter(id=request.user.id).exists() and \
            request.user.is_authenticated


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return Manager.objects.filter(id=request.user.id).exists() and \
            request.user.is_authenticated


class FormAccess(BasePermission):
    def has_permission(self, request, view):
        try:
            form = Form.objects.get(id=view.kwargs.get('form_id', 0))
        except Form.DoesNotExist:
            return False

        if request.user.id == form.doctor.id:
            return True

        if request.method == 'GET':
            return request.user.id

        return False

