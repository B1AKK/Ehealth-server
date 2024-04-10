from rest_framework import serializers
from .models import *


class EmployeeSerializer(serializers.ModelSerializer):
    manager_id = serializers.PrimaryKeyRelatedField(source='boss', queryset=Manager.objects.all())

    class Meta:
        model = Employee
        fields = ['id', 'manager_id', 'full_name', 'phone', 'address', 'status', 'med_info']


class QuestionSerializer(serializers.ModelSerializer):
    form_id = serializers.PrimaryKeyRelatedField(source='form', queryset=Form.objects.all())

    class Meta:
        model = Question
        fields = ['id', 'form_id', 'question_text', 'type', 'options']


class FormSerializer(serializers.ModelSerializer):
    doctor_id = serializers.PrimaryKeyRelatedField(source='doctor', queryset=Doctor.objects.all())
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Form
        fields = ['id', 'name', 'description', 'doctor_id', 'date', 'questions']
        depth = 1


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['text']