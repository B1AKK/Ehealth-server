# API description

**For each request except signup and login an authorization header must be provided**  
Authorization: Token xxx

## Authorization endpoints

### POST /signup
Content json: 
```json lines
{
  "role": "xxx", //employee, manager or doctor 
  "username": "xxx",
  "email": "xxx", //optional
  "password": "xxx",
  "full_name": "xxx",
  "address": "xxx",
  "phone": "xxx"
}
```


Response json:
```json
{
  "token": "xxx"
}
```

### POST /login
Content json:
```json
{
  "username": "xxx",
  "password": "xxx"
}
```
Response json:
```json
{
  "token": "xxx"
}
```


## Employee endpoints

### GET /employees/<employee_id>/notifications
Response json:
```json lines
[
  {
    "id": xxx,
    "text": "xxx",
    "manager_id": "xxx"
  },
  {
    "id": xxx,
    "text": "xxx",
    "manager_id": "xxx"
  },
  ...
]
```

### DELETE /employees/<employee_id>/notifications/<notification_id>
*Removes employee from notification targets*


### POST /employees/<employee_id>/send_answer
*Send answer to a form*

Content json:
```json lines
[
  {
    "question_id": xxx,
    "answer": ["xxx"]
  },
  {
    "question_id": xxx,
    "answer": ["xxx", "xxx", "xxx"]
  },
  ...
]
```


### PUT /employees/<employee_id>/assign_manager/<manager_code>

### PUT /employees/<employee_id>/assign_doctor/<doctor_code>

### GET /employees/<employee_id>/forms
*List of all forms assigned to employee*  
Response json: 
```json lines
[
  {"id": xxx, "date": "dd/mm/yyy"},
  {"id": xxx, "date": "dd/mm/yyy"},
  ...
]
```

### GET /employees/<employee_id>/forms/answers
*List of all forms an employee has answered*
Response json: 
```json lines
[
  {"id": xxx, "date": "dd/mm/yyy"},
  {"id": xxx, "date": "dd/mm/yyy"},
  ...
]
```


### GET /employees/<employee_id>/forms/<form_id>
Response json: 
```json lines
{
  "id": xxx,
  "name": "xxx",
  "description": "xxx",
  "doctor_id": xxx,
  "date": "dd/mm/yyy",
  "questions_data": [
    {
      "id": xxx,
      "form_id": xxx,
      "question_text": "xxx",
      "type": "rb", 
      "options": ["xxx", "xxx"]
    },
    {
      "id": xxx,
      "form_id": xxx,
      "question_text": "xxx",
      "type": "chb", 
      "options": ["xxx", "xxx"]
    },
    {
      "id": xxx,
      "form_id": xxx,
      "question_text": "xxx",
      "type": "txt",
      "options": []
    }
  ]
}
```

### GET /employees/<employee_id>/forms/<form_id>/answer
*Get an answer to the form*
Response json:
```json lines
[
  {
    "question_id": xxx,
    "answer": ["xxx", ...],
  },
  ...
]
```

### DELETE /employees/<employee_id>/forms/<form_id>
*Removes employee from form targets*

### DELETE /employees/<employee_id>/remove_manager
*Sets employee manager to None*


## Doctor endpoints

### GET /doctors/<doctor_code>
*Get id of a doctor by code*  
Response json:
```json lines
{
  "id": xxx
}
```

### PUT /doctors/<doctor_id>/update_code
*Creates new random code for doctor*  
Response json:
```json lines
{
  "code": "xxx"
}
```


### GET /doctors/<doctor_id>/patients
Response json:
```json lines
[
  {
    "id": xxx,
    "username": "xxx",
    "email": "xxx",
    "manager_id": xxx,
    "full_name": "xxx",
    "phone": "xxx",
    "address": "xxx",
    "status": "xxx",
    "med_info": "xxx"
  },
  ...
]
```


### PUT /doctors/<doctor_id>/patients/<patient_id>
*Update patient*  
Content json:
```json lines
{
  "status": "xxx",
  "med_info": "xxx"
}
```


### DELETE /doctors/<doctor_id>/patients/<patient_id>/remove
*Removes an employee from doctor's patient*


### POST /doctors/<doctor_id>/new_form
*Create a new form*  
Content json:
```json lines
{
  "name": "xxx",
  "description": "xxx",
  "targets": [id1, id2, ...],
  "questions_data": [
    {
      "question_text": "xxx",
      "type": "rb",
      "options": ["xxx", "xxx"]
    },
    {
      "question_text": "xxx",
      "type": "txt",
      "options": []
    },
    {
      "question_text": "xxx",
      "type": "chb",
      "options": ["xxx", "xxx", "xxx"]
    },
    ...
  ]
}
```

### GET /doctors/<doctor_id>/forms
*List of all forms created by a doctor*  
Response json:
```json lines
[
  {"id": xxx, "date": "dd/mm/yyy"},
  {"id": xxx, "date": "dd/mm/yyy"},
  ...
]
```


### GET /doctors/<doctor_id>/forms/<form_id>
Response json: 
```json lines
{
  "id": xxx,
  "name": "xxx",
  "description": "xxx",
  "doctor_id": xxx,
  "date": "dd/mm/yyy",
  "questions_data": [
    {
      "id": xxx,
      "form_id": xxx,
      "question_text": "xxx",
      "type": "rb", 
      "options": ["xxx", "xxx"]
    },
    {
      "id": xxx,
      "form_id": xxx,
      "question_text": "xxx",
      "type": "chb", 
      "options": ["xxx", "xxx"]
    },
    {
      "id": xxx,
      "form_id": xxx,
      "question_text": "xxx",
      "type": "txt",
      "options": []
    }
  ]
}
```


### PUT /doctors/<doctor_id>/forms/<form_id>
*Update a form*  
Content json:
```json lines
{
  "name": "xxx",
  "description": "xxx",
  "date": "dd/mm/yyy",
  "to_delete": [id1, id2, ...], //list of questions to delete
  "questions": [
    {
      "id": xxx, //update existing question
      "question_text": "xxx",
      "type": "xxx",
      "options": ["xxx", "xxx", "xxx"]
    },
    { //create new question
      "question_text": "xxx",
      "type": "xxx",
      "options": []
    }
  ]
}
```


### DELETE /doctors/<doctor_id>/forms/<form_id>
*Delete a form*


## Manager endpoints

### GET /managers/<manager_code>
*Get id of a manager by code*  
Response json:
```json lines
{
  "id": xxx
}
```


### GET /managers/<manager_id>/staff
Response json:
```json lines
[
  {
    "id": xxx,
    "username": "xxx",
    "email": "xxx",
    "manager_id": xxx,
    "full_name": "xxx",
    "phone": "xxx",
    "address": "xxx",
    "status": "xxx",
    "med_info": "xxx"
  },
  ...
]
```

### PUT /managers/<manager_id>/update_code
*Creates new random code for manager*  
Response json:
```json lines
{
  "code": "xxx"
}
```


### POST /managers/<manager_id>/create_notification
Content json:
```json lines
{
  "text": "xxx",
  "targets": [id1, id2, ...]
}
```