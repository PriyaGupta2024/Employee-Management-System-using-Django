from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .models import *
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Employee_Experience
from .models import Employee_Education
from django.shortcuts import render, redirect, get_object_or_404



# Create your views here.
def index(request):
    return render(request,'index.html')


def view_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request,'view_emp.html', context)


def add_emp (request):
    if request.method == 'POST':
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        bonus = int(request.POST['bonus'])
        phone= int(request.POST['phone'])
        email = request.POST.get('email', '')
        pwd = request.POST.get('pwd', '')
        emp_code = request.POST.get('emp_code', '')
        join_date = request.POST.get('Join_date')  
        
        new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary, dept_id=dept,  role_id = role, bonus=bonus, phone=phone, Join_date = join_date, email=email, pwd=pwd,emp_code=emp_code)
        new_emp.save()
        return HttpResponse('Employee Added Successfully')
    
    elif request.method=='GET':
        return render(request,'add_emp.html')
    else:
        return HttpResponse("An Exception Occured! Employee Has Not Been Added ")

def remove_emp(request,emp_id = 0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Successfully")
        except:
            return HttpResponse("Please Enter A Valid EMP ID")
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request,'remove_emp.html',context)


def filter_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if first_name:
            emps = emps.filter(Q(first_name__icontains = first_name) | Q(last_name__icontains = last_name))
        if dept:
            emps = emps.filter(dept__name__icontains = dept)
        
        if role:
            emps = emps.filter(role__name__icontains = role)

        context = {
            'emps': emps
        } 

        return render(request,'view_emp.html' ,context)  

    elif request.method == 'GET':
        return render(request,'filter_emp.html')


    else:
        return HttpResponse('An exception occured')
    
def Admin_home(request):
    if not request.user.is_authenticated:
        return redirect('Admin_login')
    return render(request,'Admin_home.html')

# Admin login handling
def Admin_login(request):
    error = "none"
    if request.method == 'POST':
        username =  request.POST['username']
        pwd = request.POST['pwd']
            # Authenticate the user using their username and password
        user = authenticate(username=username, password=pwd)
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                return redirect('Admin_home')  # Redirect to Admin home page if login successful
            else:
                error = 'Invalid credentials. Please try again.'
        else:
            error = 'Admin does not exist. Please check the username and. password'
        
        # Always return a response if there's an error
    return render(request, 'Admin_login.html', {'error': error})


    
def Registration(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email =  request.POST['email']
        pwd = (request.POST['pwd'])
        empcode = request.POST['emp_code']

        user = User.objects.create_user(username=email, password=pwd, email=email, first_name=first_name, last_name=last_name)
        Employee.objects.create(user = user,emp_code = empcode,first_name=first_name, last_name=last_name)
        
        Employee_Experience.objects.create(user = user)
        Employee_Education.objects.create(user = user)
        
        return  redirect('emp_login') 
    
        #except Department.DoesNotExist:
            # If the department does not exist, show an error message        
   
    return render(request,'Registration.html')

   
    
def emp_login(request):
    error = "none"
    if request.method == 'POST':
        email =  request.POST.get('email')
        pwd = request.POST.get('pwd')
        # Try to get the user by email
        try:
            user = User.objects.get(email=email)
            # Authenticate the user using their username and password
            user = authenticate(username=user.username, password=pwd)
            
            if user is not None:
                login(request, user)
                return redirect('emp_home')  # Redirect to employee home page if login successful
            else:
                error = 'Invalid credentials. Please try again.'
        except User.DoesNotExist:
            error = 'Employee does not exist. Please check the email.'
        
        # Always return a response if there's an error
        return render(request, 'emp_login.html', {'error': error})

    elif request.method == 'GET':
        # Handle GET request - render the login form
        return render(request, 'emp_login.html')

    # If request method is not POST or GET, return an error response
    return HttpResponse("An Exception Occurred! Invalid request method.", status=400)

    
    

@login_required(login_url='emp_login')  # Redirects to login if not authenticated
def emp_home(request):
    return render(request, 'emp_home.html')

def Logout(request):
    logout(request)
    return redirect('index')


@login_required(login_url='emp_login')
@transaction.atomic  # Ensures all updates are committed or rolled back
def Profile(request,uid):
    user = get_object_or_404(User, id=uid)
    employee = Employee.objects.filter(user=user).first()

    if not employee:
        messages.error(request, "Employee record not found.")
        return render(request, 'Profile.html', {'error': 'Employee record not found'})

    if request.method == 'POST':
        # ✅ Safely fetch from POST with fallback to existing value
        first_name = request.POST.get('first_name') or user.first_name
        last_name = request.POST.get('last_name') or user.last_name
        emp_code = request.POST.get('emp_code') or employee.emp_code
        cn = request.POST.get('contact') or employee.phone
        gender = request.POST.get('gender') or employee.gender
        jdate = request.POST.get('j_Date')

        user.first_name = first_name
        user.last_name = last_name
        employee.emp_code = emp_code
        employee.phone = cn
        employee.gender = gender

        if jdate:
            try:
                employee.Join_date = datetime.strptime(jdate, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "Invalid date format.")
                return render(request, 'Profile.html', {'employee': employee})

        dept_name = request.POST.get('department')
        if dept_name:
            try:
                department = Department.objects.get(name=dept_name)
                employee.dept = department
            except Department.DoesNotExist:
                messages.error(request, "Invalid department name.")
                return render(request, 'Profile.html', {'employee': employee})

        user.save()
        employee.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('Profile', uid=user.id)
    return render(request, 'Profile.html', {'employee': employee})


@login_required(login_url='emp_login')  # redirect to login if not logged in
def my_experience(request):
     user = request.user
     experience = Employee_Experience.objects.filter(user=user).first()
     if not experience:
        messages.error(request, "experience record not found.")
        
     return render(request, 'myexperience.html', {'experience': experience})

@login_required
def edit_experience(request):
    experience, _ = Employee_Experience.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        experience.Company_name1 = request.POST.get('Company_name1')
        experience.Possition1 = request.POST.get('Possition1')
        experience.salary1 = request.POST.get('salary1')
        experience.Duration1 = request.POST.get('Duration1')
        experience.Company_name2 = request.POST.get('Company_name2')
        experience.Possition2 = request.POST.get('Possition2')
        experience.salary2 = request.POST.get('salary2')
        experience.Duration2 = request.POST.get('Duration2')
        experience.Company_name3 = request.POST.get('Company_name3')
        experience.Possition3 = request.POST.get('Possition3')
        experience.salary3 = request.POST.get('salary3')
        experience.Duration3 = request.POST.get('Duration3')
        experience.save()
        return redirect('my_experience')

    return render(request, 'edit_experience.html', {'experience': experience})

def My_Education(request):
    user = request.user
    education = Employee_Education.objects.filter(user = user).first()
    if not education:
        messages.error(request,"Education record not found")

    return render(request, 'My_Education.html',{'education': education})    

def Edit_MyEducation(request):
    education, _ = Employee_Education.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        education.course_PG = request.POST.get('course_PG')
        education.clg_name_PG = request.POST.get('clg_name_PG')
        education.year_of_pass_PG = request.POST.get('year_of_pass_PG')
        education.percentage_PG = request.POST.get('percentage_PG')

        education.course_Grad = request.POST.get('course_Grad')
        education.clg_name_Grad = request.POST.get('clg_name_Grad')
        education.year_of_pass_Grad = request.POST.get('year_of_pass_Grad')
        education.percentage_Grad = request.POST.get('percentage_Grad')

        education.course_HSC = request.POST.get('course_HSC')
        education.clg_name_HSC = request.POST.get('clg_name_HSC')
        education.year_of_pass_HSC = request.POST.get('year_of_pass_HSC')
        education.percentage_HSC = request.POST.get('percentage_HSC')

        education.course_SSC = request.POST.get('course_SSC')
        education.clg_name_SSC = request.POST.get('clg_name_SSC')
        education.year_of_pass_SSC = request.POST.get('year_of_pass_SSC')
        education.percentage_SSC = request.POST.get('percentage_SSC')
        education.save()
        return redirect('My_Education')
    
    return render(request, 'Edit_MyEducation.html', {'education' : education})


def Change_pswrd(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error = ""
    user = request.user
    if request.method == 'POST':
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            if user.check_password(c):
                user.set_password(n)
                user.save()
                error = "no"
            else:
                error = "yes"
        except:
            error = "not"

    return render(request,'Change_pswrd.html',locals())


def Change_pswrdadmin(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error = ""
    user = request.user
    if request.method == 'POST':
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            if user.check_password(c):
                user.set_password(n)
                user.save()
                error = "no"
            else:
                error = "yes"
        except:
            error = "not"

    return render(request,'Change_pswrdadmin.html',locals())


def All_inone(request):
    if not request.user.is_authenticated:
        return redirect('Admin_login')
    employe = Employee.objects.all()
    return render(request,'All_inone.html',{'emps': employe})



def Edit_education(request,pid):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error = ""
    user = User.objects.get(id=pid)
    education, _ = Employee_Education.objects.get_or_create(user=user)

    if request.method == 'POST':
        education.course_PG = request.POST.get('course_PG')
        education.clg_name_PG = request.POST.get('clg_name_PG')
        education.year_of_pass_PG = request.POST.get('year_of_pass_PG')
        education.percentage_PG = request.POST.get('percentage_PG')

        education.course_Grad = request.POST.get('course_Grad')
        education.clg_name_Grad = request.POST.get('clg_name_Grad')
        education.year_of_pass_Grad = request.POST.get('year_of_pass_Grad')
        education.percentage_Grad = request.POST.get('percentage_Grad')

        education.course_HSC = request.POST.get('course_HSC')
        education.clg_name_HSC = request.POST.get('clg_name_HSC')
        education.year_of_pass_HSC = request.POST.get('year_of_pass_HSC')
        education.percentage_HSC = request.POST.get('percentage_HSC')

        education.course_SSC = request.POST.get('course_SSC')
        education.clg_name_SSC = request.POST.get('clg_name_SSC')
        education.year_of_pass_SSC = request.POST.get('year_of_pass_SSC')
        education.percentage_SSC = request.POST.get('percentage_SSC')


        try:
            education.save()
            error = "no"
        except:
            error = "yes"     
    return render(request, 'Edit_education.html', {'education' : education , 'error' : error})







       