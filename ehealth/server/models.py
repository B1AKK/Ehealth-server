from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, default="")
    phone = models.CharField(max_length=32)


class Manager(User):
    pass


class Employee(User):
    status = models.CharField(max_length=64, default="", blank=True)
    med_info = models.CharField(max_length=255, default="", blank=True)
    boss = models.ForeignKey(Manager, null=True, on_delete=models.SET_NULL, related_name="staff")

    def jsonify(self):
        return {
            "id": self.id,
            'manager_id': self.boss.id,
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
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL, related_name="forms")

    def jsonify(self):
        questions = [question.jsonify() for question in self.questions.all()]

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "doctor_id": self.doctor.id,
            "questions": questions
        }


def create_form(form_json):
    doc = Doctor.objects.get(id=form_json['doctor_id'])
    form = Form(name=form_json['name'], description=form_json['description'], doctor=doc)
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
    type = models.CharField(max_length=16, choices={
        "rb": "Radiobutton",
        "chb": "Checkbox",
        "txt": "Text",
    })
    options = models.JSONField(default=list)

    def jsonify(self):
        return {
            "id": self.id,
            'form_id': self.form.id,
            "question_text": self.question_text,
            "type": self.type,
            "options": self.options
        }


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="answers")
    answer = models.CharField(max_length=255)
