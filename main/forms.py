# forms.py
from dataclasses import fields
from django import forms
from .models import Student, Course, Feed, Assign

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['fName', 'mName', 'lName', 'sex', 'dep', 'phone', 'DOB', 'email', 'region', 'subcity', 'city', 'woreda', 'kebele']
        widgets = {
            'section': forms.NumberInput(attrs={'required': False}),
            'status': forms.ClearableFileInput(attrs={'required': False}),
        }

class SeniorSForm(forms.Form):
        id = forms.CharField(label='id')
        dep = forms.CharField(label='dep')
        section = forms.CharField(label='Section')
        year = forms.CharField(label='year')
        semi = forms.CharField(label='semi')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['ctitle', 'ccode', 'dep', 'cr_hr', 'year', 'semi', 'lec_hr', 'lab_hr', 'prerequisite', 'category']
        
        widgets = {
            'inst': forms.NumberInput(attrs={'required': False}),
        }

class AssignForm(forms.ModelForm):
    class Meta:
        model = Assign
        fields =  ['ctitle', 'ccode', 'section', 'name', 'insid']

class GetCourseForm(forms.Form):
    def __init__(self, insid, *args, **kwargs):
        super(GetCourseForm, self).__init__(*args, **kwargs)
        self.fields['course_title'] = forms.ModelChoiceField(
            queryset=Course.objects.filter(instructor_id=insid)
        )

class approvalForm(forms.Form):
    approval = forms.CharField(max_length=10)
    year = forms.CharField(max_length=10)
    semi = forms.CharField(max_length=10)
    section = forms.CharField(max_length=2)

class gradeForm(forms.Form):
    year = forms.CharField(max_length=10)
    semi = forms.CharField(max_length=10)


class FeedForm(forms.ModelForm):
    user = forms.ChoiceField(choices=(
        ('college', 'College'),
        ('department', 'Department'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    ))
    feed = forms.CharField(widget=forms.Textarea(attrs={'rows': 7}))

    class Meta:
        model = Feed
        fields = ['feed']
