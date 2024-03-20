from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, default="")
    phone = models.CharField(max_length=32)


class Manager(User):
    pass


class Employee(User):
    status = models.CharField(max_length=64, default="")
    med_info = models.CharField(max_length=255, default="")
    manager_id = models.ForeignKey(Manager, null=True, on_delete=models.SET_NULL, related_name="staff")

    def jsonify(self):
        return {
            "full_name": self.full_name,
            "phone": self.phone,
            "address": self.address,
            "status": self.status,
            "med_info": self.med_info,
        }


class Doctor(User):
    specialization = models.CharField(max_length=64)
    patients = models.ManyToManyField(Employee)


class Form(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    doctor_id = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL, related_name="forms")


class Question(models.Model):
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")
    question = models.CharField(max_length=255)
    type = models.CharField(max_length=16, choices={
        "rb": "Radiobutton",
        "chb": "Checkbox",
        "txt": "Text",
    })
    options = models.JSONField()


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="answers")
    answer = models.CharField(max_length=255)
