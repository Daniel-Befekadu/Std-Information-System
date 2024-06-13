from django.contrib import admin
from .models import Registrar, College, Department, Instructor,Student

admin.site.register(Registrar)
admin.site.register(College)
admin.site.register(Department)
admin.site.register(Instructor)
admin.site.register(Student)
