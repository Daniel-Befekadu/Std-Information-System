from django.contrib.auth.backends import ModelBackend
from main.models import Department, Instructor, Student

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, user_type=None, **kwargs):
        if user_type == 'department':
            try:
                user = Department.objects.get(dephead=username, depid=password)
                return user
            except Department.DoesNotExist:
                return None
        elif user_type == 'instructor':
            try:
                user = Instructor.objects.get(insid=username, name=password)
                return user
            except Instructor.DoesNotExist:
                return None
        elif user_type == 'student':
            try:
                user = Student.objects.get(id=username, fName=password)
                return user
            except Student.DoesNotExist:
                return None
        else:
            return None

    def get_user(self, user_id):
        pass

    def has_perm(self, user_obj, perm, obj=None):
        pass
