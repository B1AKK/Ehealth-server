from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=32)


class Manager(User):
    pass


class Employee(User):
    status = models.CharField(max_length=64)
    med_info = models.CharField(max_length=255)
    manager_id = models.ForeignKey(Manager, on_delete=models.SET_NULL, related_name="staff")


class Doctor(User):
    specialization = models.CharField(max_length=64)
    patients = models.ManyToManyField(Employee)


class Form(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.SET_NULL)


class Question(models.Model):
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    type = models.CharField(max_length=16, choices={
        "rb": "Radiobutton",
        "chb": "Checkbox",
        "txt": "Text",
    })
    options = models.JSONField()


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
