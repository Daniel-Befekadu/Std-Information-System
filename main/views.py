#from pyexpat.errors import messages
from django.shortcuts import render, redirect
from .forms import StudentForm, SeniorSForm, CourseForm, FeedForm, AssignForm, approvalForm
from .models import Student, Feed, Grade, Course, Assign, Registrar, Instructor, College, Department, Withdraw
from datetime import date
from decimal import Decimal
from django.db.models import Sum
from django.contrib import messages
from decimal import Decimal, ROUND_HALF_UP

# Create your views here.
def home(request):
    return render(request, 'home.html')

def sNavbar(request):
    return render(request, 'sNavbar.html')

def iNavbar(request):
    return render(request, 'iNavbar.html')

def dNavbar(request):
    return render(request, 'dNavbar.html')

def cNavbar(request):
    return render(request, 'cNavbar.html')

def rNavbar(request):
    return render(request, 'rNavbar.html')

def success(request):
    return render(request, 'success.html')

def submit(request):
    return render(request, 'submition.html')

def senioreg(request):
    if request.method == 'POST':
        form = SeniorSForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['id']  # Retrieve the student ID from the form's cleaned data
            dep = form.cleaned_data['dep']
            section = form.cleaned_data['section']
            year = form.cleaned_data['year']
            semi = form.cleaned_data['semi']
            student = Student.objects.get(id=student_id)
            # Retrieve the student object from the database
            try:
                student = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                messages.error(request, 'There is No Student With This ID No.') 

            try:
                cumulative = Grade.objects.get(sid=student).cumulative
            except Grade.DoesNotExist:
                cumulative = None
            if cumulative is not None and cumulative < 2.5:
                messages.error(request, 'Your Cumulative is Below The Requirment!')
            else:
                student.dep = dep
                student.section = section
                student.year = year
                student.semi = semi

            student.save()

            success_message = 'Registration successful!'
            messages.success(request, success_message)  # Redirect to a success page
    else:
        form = SeniorSForm()
    return render(request, 'senioreg.html', {'form': form})     

def freshmreg(request):
    success_message = None
    if request.method == 'POST':
        print(request.POST)
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            success_message = 'Registration successful!'
            messages.success(request, success_message)
            
        else:
            messages.error(request, 'Invalid form submission. Please check the errors!')
            print('Form is invalid:', form.errors)
    else:
        form = StudentForm()
    return render(request, 'freshmreg.html', {'form': form})

def save_feed(request):
    if request.method == 'POST':
        feed_text = request.POST.get('feed')
        user_type = request.POST.get('user')

        feed = Feed()

        if user_type == 'college':
            feed.college = feed_text
        elif user_type == 'department':
            feed.dep = feed_text
        elif user_type == 'instructor':
            feed.inst = feed_text
        elif user_type == 'student':
            feed.student = feed_text

        feed.save()

        messages.success(request, 'Posted successfully!')

    return render(request, 'announce.html')

def course(request):
    if request.method == 'POST':
        print(request.POST)
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The Course Added Successfully!')
        else:
            messages.error(request, 'Form is Invalid!')
            print('Form is invalid:', form.errors)
    else:
        form = CourseForm()
    return render(request, 'course.html', {'form': form})
    

def displaySfeed(request):
    
    current_date = date.today()

    data = Feed.objects.filter(date=current_date).exclude(student__isnull=True).values('student')

    return render(request, 'feed.html', {'data': data})
    

def displayIfeed(request):

    current_date = date.today()

    data = Feed.objects.filter(date=current_date).exclude(inst__isnull=True).values('inst')

    return render(request, 'ifeed.html', {'data': data})

def displayDfeed(request):
    
    current_date = date.today()

    data = Feed.objects.filter(date=current_date).exclude(dep__isnull=True).values('dep')

    return render(request, 'dfeed.html', {'data': data})

def displayCfeed(request):
   
    current_date = date.today()

    data = Feed.objects.filter(date=current_date).exclude(college__isnull=True).values('college')

    return render(request, 'cfeed.html', {'data': data})
    
def mygrade(request):
    
    username = request.session.get('username')

    data = Grade.objects.filter(id=username).values('student')

    return render(request, 'feed.html', {'data': data})


def submitgr(request):
    if request.method == 'POST':
        sid = request.POST.get('sid')
        ctitle = request.POST.get('ctitle')
        grade = request.POST.get('grade')
    
        course = Course.objects.get(ctitle=ctitle)
        ccode = course.ccode
        cr_hr = course.cr_hr
        year = course.year
        semi = course.semi
        student = Student.objects.get(id=sid)
        section = student.section
        dep = student.dep
        
        if grade in ['A', 'A+']:
            noGr = Decimal('4')
        elif grade == 'A-':
            noGr = Decimal('3.75')
        elif grade == 'B+':
            noGr = Decimal('3.5')
        elif grade == 'B':
            noGr = Decimal('3')
        elif grade == 'B-':
            noGr = Decimal('3.25')
        elif grade == 'C+':
            noGr = Decimal('2.5')
        elif grade == 'C':
            noGr = Decimal('2')
        elif grade == 'C-':
            noGr = Decimal('1.75')
        elif grade == 'D':
            noGr = Decimal('1')
        elif grade == 'F':
            noGr = Decimal('0')
        else: 
            noGr = Decimal('0')      
            
        grpoint = Decimal('0')

        if noGr is not None and cr_hr is not None:
            grpoint = cr_hr * Decimal(str(noGr))
            
            grade_obj, created = Grade.objects.get_or_create(sid=sid, ccode=ccode, defaults={
                'ctitle': ctitle,
                'year': year,
                'semi': semi,
                'section': section,
                'dep': dep,
                'cr_hr': cr_hr,
                'noGr': noGr,
                'grade': grade,
                'grpoint': grpoint if noGr != 'NG' else 'invalid',
                'approval': 'Pending'
            })
            
            if not created:
                grade_obj.ctitle = ctitle
                grade_obj.year = year
                grade_obj.semi = semi
                grade_obj.section = section
                grade_obj.dep = dep
                grade_obj.cr_hr = cr_hr
                grade_obj.noGr = noGr
                grade_obj.grade = grade
                grade_obj.grpoint = grpoint
                grade_obj.approval = 'Pending'
                grade_obj.save()
        else:
            messages.error(request, 'No Credit or Invalid Form!')
        
    insid = request.session.get('insid')
    course_list = Assign.objects.filter(insid=insid)        
    return render(request, 'submition.html', {'course_list': course_list})

def AssignInst(request):
    if request.method == 'POST':
        ctitle = request.POST.get('ctitle')
        ccode = request.POST.get('ccode')
        section = request.POST.get('section')
        name = request.POST.get('name')
        insid = request.POST.get('insid')
        dep = request.session.get('dep')

        assign = Assign(ctitle=ctitle, ccode=ccode, section=section, name=name, insid=insid, dep=dep)
        assign.save()
        
        messages.success(request, 'Teacher Assigned Successfully!')

    return render(request, 'assign.html',)



def signup(request):
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if user_type == 'register':
         
            try:
                registrar = Registrar.objects.get(regid=username, passwd=password)
                reg_obj = Registrar.objects.filter(passwd=password).values('regid').first()
                print(reg_obj)
        
                if reg_obj:
                    regid = reg_obj.get('regid')  
                    request.session['regid'] = regid
                    return redirect('rNavbar')
                else:
                    messages.error(request, 'Multiple user!')   
            except Registrar.DoesNotExist:
                messages.error(request, 'INCORRECT USERNAME OR PASSWORD!')
                pass
            
        elif user_type == 'college':
            
            try:
                college = College.objects.get(collegeid=username, passwd=password)
                coll_obj = College.objects.filter(passwd=password).values('collegeid').first()
                colldep = Department.objects.filter(collegeid=coll_obj).values('dep')
                print(coll_obj)
        
                if coll_obj:
                    collegeid = coll_obj.get('collegeid') 
                    request.session['collegeid'] = collegeid
                    return redirect('cfeed')
                else:
                    messages.error(request, 'Multiple user!')                    
            except College.DoesNotExist:
                messages.error(request, 'INCORRECT USERNAME OR PASSWORD!')
                pass
            
        elif user_type == 'department':
            
            try:
                department = Department.objects.get(depid=username, passwd=password)
                dep_obj = Department.objects.filter(passwd=password).values('dep').first()

                if dep_obj:
                    dep = dep_obj.get('dep')  
                    request.session['dep'] = dep
                    return redirect('dfeed')
                else:
                    messages.error(request, 'Multiple user!')   
            except Department.DoesNotExist:
                messages.error(request, 'INCORRECT USERNAME OR PASSWORD!')
                pass
            
        elif user_type == 'instructor':
           
            try:
                instructor = Instructor.objects.get(insid=username, passwd=password)
                ins_obj = Instructor.objects.filter(passwd=password).values('insid').first()
                print(ins_obj)

                if ins_obj:
                    insid = ins_obj.get('insid')  
                    request.session['insid'] = insid
                    return redirect('ifeed')
                else:
                    messages.error(request, 'Multiple user!')   
            except Instructor.DoesNotExist:
                messages.error(request, 'INCORRECT USERNAME OR PASSWORD!')
                pass
            
        elif user_type == 'student':
         
            try:
                student = Student.objects.get(id=username, passwd=password)
                stud_obj = Student.objects.filter(passwd=password).values('id').first()
                print(student)
                if stud_obj:
                    id = stud_obj.get('id')
                    request.session['id'] = id
                    return redirect('feed')
                else:
                    messages.error(request, 'Multiple user!') 
            except Student.DoesNotExist:
                messages.error(request, 'INCORRECT USERNAME OR PASSWORD!')
                pass
    
    return render(request, 'login.html')

def approval(request):
    if request.method == 'POST':
        form = approvalForm(request.POST)
        if form.is_valid():
            approval = form.cleaned_data['approval']
            year = request.POST.get('year')
            semi = request.POST.get('semi')
            section = request.POST.get('section')
            #section = request.POST.get('section')
            
            if approval == 'Approved':
                Grade.objects.filter().update(approval=approval)
                grades = Grade.objects.values('sid').distinct()
                depart = request.session.get('dep')
                for grade in grades:
                    sid = grade['sid']

                    
                    total_grpoint = Grade.objects.filter(sid=sid, year=year, semi=semi, section=section, dep=depart).aggregate(Sum('grpoint'))['grpoint__sum']
                    total_cr_hr = Grade.objects.filter(sid=sid, year=year, semi=semi, section=section, dep=depart).aggregate(Sum('cr_hr'))['cr_hr__sum']
                    semigrade = Decimal('0')
                    
                    if total_grpoint is not None and total_cr_hr is not None:
                        semigrade = total_grpoint / total_cr_hr
                    
                    if total_grpoint is None:
                        semigrade = 0
                    
                    Grade.objects.filter(sid=sid, year=year, semi=semi, dep=depart, section=section,).update(semigrade=semigrade)
                    print(semigrade)
                sids = Grade.objects.values('sid').distinct()
                for sid in sids:
                    sid = sid['sid']
                    
                    total_grpoint_sid = Grade.objects.filter(sid=sid, dep=depart).aggregate(Sum('grpoint'))['grpoint__sum']
                    total_cr_hr_sid = Grade.objects.filter(sid=sid, dep=depart).aggregate(Sum('cr_hr'))['cr_hr__sum']
                    
                    cumulative = Decimal('0')
                    
                    if total_grpoint_sid is not None and total_cr_hr_sid is not None:
                        cumulative = total_grpoint_sid / total_cr_hr_sid
                    
                    if total_grpoint_sid is None:
                        cumulative = 0
                    
                    Grade.objects.filter(sid=sid, dep=depart).update(cumulative=cumulative)
                
                messages.success(request, 'GRADE APPROVED SUCCESSFULLY!')
            else:
                messages.error(request, 'GRADE REJECTED!')
    else:
        form = approvalForm()
    
    return render(request, 'approval.html', {'form': form})

def withdrawal_form(request):
    message = None
    if request.method == 'POST':
        fName = request.POST.get('fName')
        mName = request.POST.get('mName')
        lName = request.POST.get('lName')
        year = request.POST.get('year')
        stuid = request.POST.get('stuid')
        department = request.POST.get('department')
        reason = request.POST.get('reason')
        evid = request.FILES.get('evid')
        
        withdrawal = Withdraw(fName=fName, mName=mName, lName=lName, year=year, stuid=stuid, department=department, reason=reason, evid=evid)
        withdrawal.save()
        
        message=messages.success(request, 'Yor Withdrawal Form Sent.')

    return render(request, 'withdraw.html', {'message':message})

def view_withdraw(request):
    current_date = date.today() 
    data = Withdraw.objects.filter(date=current_date)
    return render(request, 'view_withdrwal.html', {'data': data})

def ViewMyGrade(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        semi = request.POST.get('semi')
        return redirect('grade_list', year=year, semi=semi)
    
    return render(request, 'mygrade.html')

def grade_list(request, year, semi):

    id = request.session.get('id')
    grade = Grade.objects.filter(sid=id, year=year, semi=semi)
    context = {
        'grade': grade
    }
    return render(request, 'ViewMyGrade.html', context)

def ViewCollGrade(request):
    if request.method == 'POST':
        dep = request.POST.get('dep')
        year = request.POST.get('year')
        semi = request.POST.get('semi')
        return redirect('collgrade_list', dep=dep, year=year, semi=semi)
    '''colldep = request.session.get('dep')
    dep_list = Department.objects.filter(dep=colldep) '''
    return render(request, 'Collgrade.html')

def collgrade_list(request, dep, year, semi):

    grade = Grade.objects.filter(dep=dep, year=year, semi=semi)
    context = {
        'grade': grade
    }
    return render(request, 'ViewCollGrade.html', context)

def ViewDepGrade(request):
    if request.method == 'POST':
        dep = request.POST.get('dep')
        year = request.POST.get('year')
        semi = request.POST.get('semi')
        return redirect('depgrade_list', dep=dep, year=year, semi=semi)
    '''colldep = request.session.get('dep')
    dep_list = Department.objects.filter(dep=colldep) '''
    return render(request, 'DepGrade.html')

def depgrade_list(request, dep, year, semi):

    colldep = request.session.get('dep')
    grade = Grade.objects.filter(dep=dep, year=year, semi=semi)
    context = {
        'grade': grade
    }
    return render(request, 'ViewDepGrade.html', context)

def ViewStuGrade(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        semi = request.POST.get('semi')
        return redirect('stugrade_list', year=year, semi=semi)
    
    return render(request, 'StuGrade.html')

def stugrade_list(request, year, semi):

    dep = request.session.get('dep')
    grade = Grade.objects.filter(dep=dep, year=year, semi=semi)
    context = {
        'grade': grade
    }
    return render(request, 'ViewStuGrade.html', context)

def course_list(request):
    if request.method == 'POST':
        dep = request.POST.get('dep')
        year = request.POST.get('year')
        semi = request.POST.get('semi')
        return redirect('course_list', dep=dep, year=year, semi=semi)
    
    return render(request, 'MyCourse.html')

def ViewCourse(request, dep, year, semi):

    course = Course.objects.filter(dep=dep, year=year, semi=semi)
    context = {
        'course' : course
    }
    return render(request, 'ViewCourse.html', context)

def AddCollege(request):
    if request.method == 'POST':
        college = request.POST.get('college')
        collegedean = request.POST.get('collegedean')
        collegeid = request.POST.get('collegeid')
        if College.objects.filter(collegeid=collegeid).exists():
            messages.error(request, 'College ID Already Exist.')

        college = College(college=college, collegedean=collegedean, collegeid=collegeid)
        college.save()
        messages.success(request, 'College Registered Successfully!')
    return render(request, 'AddCollege.html')

def AddDep(request):
    if request.method == 'POST':
        dep = request.POST.get('dep')
        depid = request.POST.get('depid')
        dephead = request.POST.get('dephead')
        college = request.POST.get('college')
        collegeid = request.POST.get('collegeid')
        if Department.objects.filter(depid=depid).exists():
            messages.error(request, 'Department ID Already Exist.')

        department = Department(dep=dep, depid=depid, dephead=dephead, college=college, collegeid=collegeid)
        department.save()
        messages.success(request, 'Department Registered Successfully!')
    return render(request, 'AddDep.html')

def AddIns(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        insid = request.POST.get('insid')
        dep = request.POST.get('dep')
        if Instructor.objects.filter(insid=insid).exists():
            messages.error(request, 'Instructor ID Already Exist.')

        instructor = Instructor(name=name, insid=insid, dep=dep)
        instructor.save()
        messages.success(request, 'Instructor Registered.')
        messages.success(request, 'Instructor Registered Successfully!')
    return render(request, 'AddIns.html')

def passwordchange(request):
    if request.method == 'POST':
        current_password = request.POST.get('crpasswd')
        new_password = request.POST.get('passwd')
        confirmpassword = request.POST.get('conpasswd')
        try:
            student = Student.objects.get(passwd=current_password)
        except Student.DoesNotExist:
            messages.error(request, 'Student Not Found')
            return render(request, 'sPasswdChange.html')

        student = Student.objects.get(passwd=current_password)
        if new_password == confirmpassword:

            if student.passwd == current_password:
                student.passwd = new_password
                student.save()
                messages.success(request, 'Password Changed Successfully!')
            else:
                messages.error(request, 'Wrong Password!')
        else:
            messages.error(request, 'The Password Does Not Match!')

    return render(request, 'sPasswdChange.html')

def Ipasswordchange(request):
    if request.method == 'POST':
        current_password = request.POST.get('crpasswd')
        new_password = request.POST.get('passwd')
        confirmpassword = request.POST.get('conpasswd')

        try:
            instructor = Instructor.objects.get(passwd=current_password)
        except Instructor.DoesNotExist:
            messages.error(request, 'User Not Found')
            return render(request, 'iPasswdChange.html')
        
        instructor = Instructor.objects.get(passwd=current_password)
        if new_password == confirmpassword:

            if instructor.passwd == current_password:
                instructor.passwd = new_password
                instructor.save()
                messages.success(request, 'Password Changed Successfully!')
                
            else:
                messages.error(request, 'Wrong Password!')
        else:
            messages.error(request, 'The Password Does Not Match!')

    return render(request, 'iPasswdChange.html')

def Dpasswordchange(request):
    if request.method == 'POST':
        current_password = request.POST.get('crpasswd')
        new_password = request.POST.get('passwd')
        confirmpassword = request.POST.get('conpasswd')

        try:
            department = Department.objects.get(passwd=current_password)
        except Department.DoesNotExist:
            messages.error(request, 'User Not Found')
            return render(request, 'dPasswdChange.html')

        department = Department.objects.get(passwd=current_password)
        if new_password == confirmpassword:

            if department.passwd == current_password:
                department.passwd = new_password
                department.save()
                messages.success(request, 'Password Changed Successfully!')
            else:
                messages.error(request, 'Wrong Password!')
        else:
            messages.error(request, 'The Password Does Not Match!')

    return render(request, 'dPasswdChange.html')

def Cpasswordchange(request):
    if request.method == 'POST':
        current_password = request.POST.get('crpasswd')
        new_password = request.POST.get('passwd')
        confirmpassword = request.POST.get('conpasswd')
        try:
            college = College.objects.get(passwd=current_password)
        except College.DoesNotExist:
            messages.error(request, 'User Not Found')
            return render(request, 'cPasswdChange.html')
        
        college = College.objects.get(passwd=current_password)
        if new_password == confirmpassword:
            if college.passwd == current_password:
                college.passwd = new_password
                college.save()
                messages.success(request, 'Password Changed Successfully!')
                
            else:
                messages.error(request, 'Wrong Password!')

        else:
            messages.error(request, 'The Password Does Not Match!')
    return render(request, 'cPasswdChange.html')

def Rpasswordchange(request):
    if request.method == 'POST':
        current_password = request.POST.get('crpasswd')
        new_password = request.POST.get('passwd')
        confirmpassword = request.POST.get('conpasswd')
        try:
            registrar = Registrar.objects.get(passwd=current_password)
        except Registrar.DoesNotExist:
            messages.error(request, 'User Not Found')
            return render(request, 'rPasswdChange.html')
        registrar = Registrar.objects.get(passwd=current_password)
        if new_password == confirmpassword:
            if registrar.passwd == current_password:
                registrar.passwd = new_password
                registrar.save()
                messages.success(request, 'Password Changed Successfully!')
                
            else:
                messages.error(request, 'Wrong Password!')
        else:
            messages.error(request, 'The Password Does Not Match!')
            
    return render(request, 'rPasswdChange.html')

def collApproval(request):
    if request.method == 'POST':
        dep = request.POST.get('dep')
        year = request.POST.get('year')
        semi = request.POST.get('semi')
        approval = request.POST.get('approval')

        grades = Grade.objects.filter(dep=dep, year=year, semi=semi)

        for grade in grades:
            grade.collapproval = approval
            grade.save()

        success_message = 'Grade Approved'
        messages.success(request, success_message)
    else:
        messages.error(request, 'Invalid form submission. Please check!')
    return render(request, 'collegeapproval.html') 

def ViewStudent(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        semi = request.POST.get('semi')
        return redirect('Student_list', year=year, semi=semi)
    
    return render(request, 'Stuinfo.html')

def Student_list(request, year, semi):

    dep = request.session.get('dep')
    student = Student.objects.filter(dep=dep, year=year, semi=semi)
    context = {
        'student': student
    }
    return render(request, 'ViewStudents.html', context)
    
def ViewAllStu(request):
    if request.method == 'POST':
        dep = request.POST.get('dep')
        year = request.POST.get('year')
        semi = request.POST.get('semi')
        return redirect('allStu_list', dep=dep, year=year, semi=semi)

    return render(request, 'AllStu.html')

def allStu_list(request, dep, year, semi):

    student = Student.objects.filter(dep=dep, year=year, semi=semi)
    context = {
        'student': student
    }
    return render(request, 'ViewAllStudents.html', context)

def ViewIns(request):
    if request.method == 'POST':
        dep = request.POST.get('dep')
        return redirect('ins_list', dep=dep)

    return render(request, 'insinfo.html')

def ins_list(request, dep):

    instructor = Instructor.objects.filter(dep=dep)
    context = {
        'instructor': instructor
    }
    return render(request, 'ViewAllIns.html', context)

def ViewDep(request):
    department = Department.objects.all()
    return render(request, 'ViewDep.html', {'department': department})

def ViewColl(request):
    college = College.objects.all()
    return render(request, 'ViewColl.html', {'college': college})

def ViewAssign(request):
    dep = request.session.get('dep')
    assign = Assign.objects.filter(dep=dep)
    return render(request, 'ViewAssign.html', {'assign': assign})

def ViewMyIns(request):
    dep = request.session.get('dep')
    ins = Instructor.objects.filter(dep=dep)
    return render(request, 'ViewMyIns.html', {'ins': ins})

def ViewCollIns(request):
    if request.method == 'POST':
        dep = request.POST.get('dep')
        return redirect('collIns_list', dep=dep)

    return render(request, 'collInsinfo.html')

def collIns_list(request, dep):

    instructor = Instructor.objects.filter(dep=dep)
    context = {
        'instructor': instructor
    }
    return render(request, 'ViewCollIns.html', context)

def ViewMyDep(request):
    collegeid = request.session.get('collegeid')
    dep = Department.objects.filter(collegeid=collegeid)
    return render(request, 'ViewMyDep.html', {'dep': dep})
