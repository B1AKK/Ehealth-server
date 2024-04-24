from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
import random
import string

DATE_FORMAT = '%d/%m/%Y'


def random_code():
    while True:
        code = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=16))
        if not (Manager.objects.filter(code=code).exists() or Doctor.objects.filter(code=code).exists()):
            return code


class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, default="")
    phone = models.CharField(max_length=32)

    @property
    def role(self):
        if Employee.objects.filter(id=self.id).exists():
            return 'employee'
        if Manager.objects.filter(id=self.id).exists():
            return 'manager'
        if Doctor.objects.filter(id=self.id).exists():
            return 'doctor'
        return 'unknown'



class Manager(User):
    code = models.CharField(max_length=16, unique=True, default=random_code)

    class Meta:
        db_table = 'manager_table'


class Employee(User):
    status = models.CharField(max_length=64, default="", blank=True)
    med_info = models.CharField(max_length=255, default="", blank=True)
    boss = models.ForeignKey(Manager, blank=True, null=True, on_delete=models.SET_NULL, related_name="staff")

    class Meta:
        db_table = 'employee_table'
    # last updated



class Doctor(User):
    specialization = models.CharField(max_length=64)
    patients = models.ManyToManyField(Employee, blank=True)
    code = models.CharField(max_length=16, unique=True, default=random_code)

    class Meta:
        db_table = 'doctor_table'


class Form(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL, related_name="forms")
    date = models.DateTimeField(null=True, blank=True)
    targets = models.ManyToManyField(Employee, related_name='forms')



def create_form(form_json):
    doc = Doctor.objects.get(id=form_json['doctor_id'])
    form = Form(
        name=form_json['name'],
        description=form_json['description'],
        doctor=doc,
        date=datetime.strptime(form_json['date'], DATE_FORMAT)
    )
    questions = form_json['questions']
    form.save()

    for question in questions:
        Question(
            form=form,
            question_text=question["question_text"],
            type=question["type"],
            options=question["options"],
        ).save()


def update_form(form_json, form_id):
    form = Form.objects.get(id=form_id)
    form.name = form_json['name']
    form.description = form_json['description']
    for question_json in form_json['questions']:
        if 'id' in question_json:
            question = Question.objects.get(id=question_json['id'])
            question.question_text = question_json['question_text']
            question.type = question_json['type']
            question.options = question_json['options']
            question.save()
        else:
            Question(
                form=form,
                question_text=question_json["question_text"],
                type=question_json["type"],
                options=question_json["options"],
            ).save()

    form.save()


class Question(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=255)
    type = models.CharField(max_length=3, choices={
        "rb": "Radiobutton",
        "chb": "Checkbox",
        "txt": "Text",
    })
    options = models.JSONField(default=list)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="answers")
    answer = models.JSONField()


class Notification(models.Model):
    text = models.CharField(max_length=255)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='notifications')
    targets = models.ManyToManyField(Employee, related_name='notifications')

