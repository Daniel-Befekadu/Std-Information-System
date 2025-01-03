from django.db import models
from django.utils import timezone
import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from decimal import Decimal

class Registrar(models.Model):
    name = models.CharField(max_length=100, null=True)
    regid= models.CharField(max_length=10, primary_key=True)
    passwd = models.CharField(max_length=100, null= True)
    def save(self, *args, **kwargs):
        if not self.passwd:
            self.passwd = self.regid
        super(Registrar, self).save(*args, **kwargs)

class College(models.Model):
    college = models.CharField(max_length= 100, null=True)
    collegedean = models.CharField(max_length=100, null=True)
    collegeid = models.CharField(max_length=10, primary_key=True)
    passwd = models.CharField(max_length=100, null= True)
    def save(self, *args, **kwargs):
        if not self.passwd:
            self.passwd = self.collegeid
        super(College, self).save(*args, **kwargs)

class Department(models.Model):
    dep = models.CharField(max_length=25, null=True)
    depid = models.CharField(max_length=10, primary_key=True)
    dephead = models.CharField(max_length=100, null=True)
    college = models.CharField(max_length=100, null=True)
    collegeid = models.CharField(max_length=100, null=True)
    passwd = models.CharField(max_length=100, null= True)
    def save(self, *args, **kwargs):
        if not self.passwd:
            self.passwd = self.depid
        super(Department, self).save(*args, **kwargs)

class Instructor(models.Model):
    name = models.CharField(max_length=100, null=True)
    insid = models.CharField(max_length=10, primary_key=True)
    dep = models.CharField(max_length=100, null=True)
    passwd = models.CharField(max_length=100, null= True)

    def save(self, *args, **kwargs):
        if not self.passwd:
            self.passwd = self.insid
        super(Instructor, self).save(*args, **kwargs)

class Student(models.Model):
    '''YEAR_CHOICES = (
        ('1st', '1st'),
        ('2nd', '2nd'),
        ('3rd', '3rd'),
        ('4th', '4th'),
    )
    SEMI_CHOICES = (
        ('1st', '1st'),
        ('2nd', '2nd'),
    )'''
    id = models.CharField(max_length=100, primary_key=True)
    fName = models.CharField(max_length=100, null= True)
    mName = models.CharField(max_length=100, null= True)
    lName = models.CharField(max_length=100, null= True)
    sex = models.CharField(max_length=7, null= True)
    dep = models.CharField(max_length=100, null= True)
    section = models.CharField(max_length=2, default='A')
    year = models.CharField(max_length=5, default='1st')
    semi = models.CharField(max_length=5, default='1st')
    DOB = models.DateField(null= True)
    region = models.CharField(max_length=100, null= True)
    subcity = models.CharField(max_length=100, null= True)
    city = models.CharField(max_length=100, null= True)
    woreda = models.CharField(max_length=100, null= True)
    kebele = models.CharField(max_length=10, null= True)
    email = models.EmailField(unique=True, null= True)
    phone = models.CharField(max_length=50, null= True)
    passwd = models.CharField(max_length=100, null= True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            current_year = datetime.datetime.now().year % 100
            last_student = Student.objects.filter(id__endswith=f"/{current_year}").order_by('-id').first()

            if last_student:
                last_id_parts = last_student.id.split('/')
                if len(last_id_parts) == 3:
                    last_number = int(last_id_parts[1])
                else:
                    last_number = 0
            else:
                last_number = 0

            new_number = last_number + 1
            new_id = f"R/{new_number:04d}/{str(current_year)}"
            self.id = new_id

        super().save(*args, **kwargs)
    def set_default_passwd(self):
        if not self.passwd:
            self.passwd = self.id

@receiver(pre_save, sender=Student)
def set_default_passwd(sender, instance, **kwargs):
    instance.set_default_passwd()       
    
class Grade(models.Model):
    sid = models.CharField(max_length=25, null=True)
    ctitle = models.CharField(max_length=25,null= True)
    ccode = models.CharField(max_length=10, null= True)
    cr_hr = models.IntegerField(null= True)
    dep = models.CharField(max_length=50, null= True)
    year = models.CharField(max_length=10, null= True)
    semi = models.CharField(max_length=10, null= True)
    section = models.CharField(max_length=2, null= True)
    noGr = models.DecimalField(max_digits=5, decimal_places=2, null= True)
    grade = models.CharField(max_length=10, null= True)
    grpoint = models.DecimalField(max_digits=5, decimal_places=2, null= True)
    semigrade = models.DecimalField(max_digits=5, decimal_places=2, null= True)
    cumulative = models.DecimalField(max_digits=5, decimal_places=2, null= True)
    approval = models.CharField(max_length=10, null= True)
    collapproval = models.CharField(max_length=10, null= True)

class Feed(models.Model):
    college = models.CharField(max_length=1000, null= True)
    dep = models.CharField(max_length=1000, null= True)
    inst = models.CharField(max_length=1000, null= True)
    student = models.CharField(max_length=1000, null= True)
    date = models.DateField(auto_now_add=True, null= True)

class Withdraw(models.Model):
    fName = models.CharField(max_length=100, null= True)
    mName = models.CharField(max_length=100, null= True)
    lName = models.CharField(max_length=100, null= True)
    year = models.CharField(max_length=10, null= True)
    stuid = models.CharField(max_length=100, null= True)
    department = models.CharField(max_length=100, null= True)
    reason = models.CharField(max_length=1000, null= True)
    evid = models.FileField(upload_to='pdf_files/', null= True)
    date = models.DateField(auto_now_add=True, null= True)

class Course(models.Model):
    ctitle = models.CharField(max_length=50,null= True)
    ccode = models.CharField(primary_key=True, max_length=10)
    cr_hr = models.IntegerField(null= True)
    dep = models.CharField(max_length=50, null= True)
    year = models.CharField(max_length=10, null= True)
    semi = models.CharField(max_length=10, null= True)
    lec_hr = models.IntegerField(null= True)
    lab_hr = models.IntegerField(null= True)
    prerequisite = models.CharField(max_length=10, null= True)
    category = models.CharField(max_length=20, null= True)

class Assign(models.Model):
    ctitle = models.CharField(max_length=50,null= True)
    ccode = models.CharField(primary_key=True, max_length=10)
    section = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    insid = models.CharField(max_length=10, null=True)
    dep = models.CharField(max_length=100, null=True)
 
