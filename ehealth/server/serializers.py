from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'address', 'phone']


class EmployeeSerializer(serializers.ModelSerializer):
    manager_id = serializers.PrimaryKeyRelatedField(source='boss', read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(source='assigned_doctor', read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'username', 'password', 'email',
                  'manager_id', 'doctor_id', 'full_name', 'phone', 'address', 'status', 'med_info']


class QuestionSerializer(serializers.ModelSerializer):
    form_id = serializers.PrimaryKeyRelatedField(queryset=Form.objects.all(), source='form', required=False)
    id = serializers.IntegerField(read_only=False, required=False)

    class Meta:
        model = Question
        fields = ['id', 'form_id', 'question_text', 'type', 'options']


class FormSerializer(serializers.ModelSerializer):
    doctor_id = serializers.PrimaryKeyRelatedField(source='doctor', queryset=Doctor.objects.all())
    questions = QuestionSerializer(many=True, required=False)
    date = serializers.SerializerMethodField()
    targets = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), many=True, required=False)
    to_delete = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), many=True, required=False, write_only=True)

    class Meta:
        model = Form
        fields = ['id', 'name', 'description', 'doctor_id', 'date', 'targets', 'questions', 'to_delete']


    def validate(self, attrs):
        doctor = attrs['doctor']
        targets = attrs.get('targets', list())
        for target in targets:
            if not doctor.patients.filter(id=target.id).exists():
                raise ValidationError(f'Employee {target.id} is not a patient of doctor {doctor.id}')
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('to_delete', None)

        date_str = validated_data.get('date', datetime.now().strftime(DATE_FORMAT))
        validated_data['date'] = datetime.strptime(date_str, DATE_FORMAT)

        targets_data = validated_data.pop('targets', list())
        questions_data = validated_data.pop('questions', list())

        form = Form.objects.create(**validated_data)

        form.targets.set(targets_data)

        for question_data in questions_data:
            question_data.pop(id, None)
            Question.objects.create(form=form, **question_data)

        return form

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', list())
        to_delete = validated_data.pop('to_delete', list())
        instance = super().update(instance, validated_data)

        for question in to_delete:
            question.delete()

        for question_data in questions_data:
            question_data['form_id'] = instance.id
            id = question_data['id']
            if id > 0:
                try:
                    question = instance.questions.get(id=question_data['id'])
                except Question.DoesNotExist:
                    raise NotFound(f'Question({question_data["id"]}) not found')
                question_serializer = QuestionSerializer(question, data=question_data, partial=True)

            else:
                question_data.pop('id')
                question_serializer = QuestionSerializer(data=question_data)

            if not question_serializer.is_valid():
                print('validity check failed', question_serializer.errors)
                raise ValidationError(question_serializer.errors)
            question_serializer.save()

        return instance

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
    employee_id = serializers.PrimaryKeyRelatedField(source='employee', queryset=Employee.objects.all(), write_only=True)

    class Meta:
        model = Answer
        fields = ['question_id', 'employee_id', 'answer']


    def validate(self, attrs):
        attrs = super().validate(attrs)
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

