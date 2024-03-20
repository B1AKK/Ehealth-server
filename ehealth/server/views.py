from django.shortcuts import render
from django.http import JsonResponse
from .models import *


def get_all_employees(request):
    employees = Employee.objects.all()
    res = []
    for employee in employees:
        res.append(employee.jsonify())
    return JsonResponse(res, safe=False)

