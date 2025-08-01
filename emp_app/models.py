from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100)


    def __str__(self):
        return self.name 


class Role(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name 



class Employee(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Nullable for admin-added employees
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100)
    emp_code = models.CharField(max_length=100)
    dept = models.ForeignKey(Department,on_delete=models.SET_NULL, null=True, blank=True)
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    role = models.ForeignKey(Role,on_delete=models.CASCADE ,default=1)
    phone = models.IntegerField(default=0)
    Join_date = models.DateField(null=True)
    email = models.EmailField()
    pwd= models.CharField(max_length=100)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    



    def __str__(self):
        return "%s  %s " %(self.first_name,self.last_name,)   



class Employee_Education(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Nullable for admin-added employees
    course_PG = models.CharField(max_length=100, null=True)
    clg_name_PG = models.CharField(max_length=200, null=True)
    year_of_pass_PG = models.CharField(max_length=50,null=True)
    percentage_PG = models.CharField(max_length=50,null=True)

    course_Grad= models.CharField(max_length=100, null=True)
    clg_name_Grad = models.CharField(max_length=200, null=True)
    year_of_pass_Grad = models.CharField(max_length=50,null=True)
    percentage_Grad = models.CharField(max_length=50,null=True)

    course_HSC = models.CharField(max_length=100, null=True)
    clg_name_HSC= models.CharField(max_length=200, null=True)
    year_of_pass_HSC = models.CharField(max_length=50,null=True)
    percentage_HSC = models.CharField(max_length=50,null=True)

    course_SSC = models.CharField(max_length=100, null=True)
    clg_name_SSC = models.CharField(max_length=200, null=True)
    year_of_pass_SSC= models.CharField(max_length=50,null=True)
    percentage_SSC = models.CharField(max_length=50,null=True)
    



    def __str__(self):
        return "%s  %s " %(self.user.username,self.course_PG,)  


class Employee_Experience(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Nullable for admin-added employees
    Company_name1 = models.CharField(max_length=100, null=True)
    Possition1 = models.CharField(max_length=100, null=True)
    salary1= models.CharField(max_length=100,null=True)
    Duration1 = models.CharField(max_length=100,null=True)

    Company_name2 = models.CharField(max_length=100, null=True)
    Possition2 = models.CharField(max_length=100, null=True)
    salary2 = models.CharField(max_length=100,null=True)
    Duration2 = models.CharField(max_length=100,null=True)

    Company_name3 = models.CharField(max_length=100, null=True)
    Possition3 = models.CharField(max_length=100, null=True)
    salary3 = models.CharField(max_length=100,null=True)
    Duration3 = models.CharField(max_length=100,null=True)

    
    



    def __str__(self):
        return f"{self.user.username} - {self.Company_name1}"