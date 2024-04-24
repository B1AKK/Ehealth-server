from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'address', 'phone']


class EmployeeSerializer(serializers.ModelSerializer):
    manager_id = serializers.PrimaryKeyRelatedField(source='boss', queryset=Manager.objects.all(), required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'username', 'password', 'email',
                  'manager_id', 'full_name', 'phone', 'address', 'status', 'med_info']


class QuestionSerializer(serializers.ModelSerializer):
    form_id = serializers.PrimaryKeyRelatedField(source='form', queryset=Form.objects.all())

    class Meta:
        model = Question
        fields = ['id', 'form_id', 'question_text', 'type', 'options']


class FormSerializer(serializers.ModelSerializer):
    doctor_id = serializers.PrimaryKeyRelatedField(source='doctor', queryset=Doctor.objects.all())
    questions = QuestionSerializer(many=True, required=False)
    date = serializers.SerializerMethodField()
    targets = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), many=True, required=False,
                                                 write_only=True)

    class Meta:
        model = Form
        fields = ['id', 'name', 'description', 'doctor_id', 'date', 'targets', 'questions']

    def create(self, validated_data):
        date_str = validated_data.get('date', datetime.now().strftime(DATE_FORMAT))
        validated_data['date'] = datetime.strptime(date_str, DATE_FORMAT)
        return Form.objects.create(**validated_data)

    def get_date(self, obj):
        return obj.date.strftime(DATE_FORMAT)


class ManagerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Manager
        fields = ['id', 'username', 'password', 'email', 'code',
                  'full_name', 'address', 'phone']


class DoctorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'username', 'password', 'email', 'code',
                  'full_name', 'specialization', 'address', 'phone']


class NotificationSerializer(serializers.ModelSerializer):
    targets = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), many=True, required=False,
                                                 write_only=True)
    manager_id = serializers.PrimaryKeyRelatedField(source='manager', queryset=Manager.objects.all())

    class Meta:
        model = Notification
        fields = ['id', 'text', 'manager_id', 'targets']

    def create(self, validated_data):
        targets = validated_data.pop('targets', [])
        notification = Notification.objects.create(**validated_data)
        for employee in targets:
            # employee = Employee.objects.get(id=id)
            notification.targets.add(employee)
        return notification


class AnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(source='question', queryset=Question.objects.all())
    employee_id = serializers.PrimaryKeyRelatedField(source='employee', queryset=Employee.objects.all())

    class Meta:
        model = Answer
        fields = ['question_id', 'employee_id', 'answer']


    def validate(self, attrs):
        question = attrs['question']
        answer_list = attrs['answer']
        if question.type == 'rb':
            if len(answer_list) != 1:
                raise ValidationError('RadioButtons must have exactly one answer')
            if answer_list[0] not in question.options:
                raise ValidationError('Answer not in options')
        elif question.type == 'chb':
            for answer in answer_list:
                if answer not in question.options:
                    raise ValidationError('Answer not in options')

        else:
            if len(answer_list) != 1:
                raise ValidationError('Text answer must have exactly one element')

        return attrs

