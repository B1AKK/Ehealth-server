from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Manager)
admin.site.register(Doctor)
admin.site.register(Form)
admin.site.register(Notification)
admin.site.register(Answer)
