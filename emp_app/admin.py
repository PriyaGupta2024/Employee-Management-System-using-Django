from django.contrib import admin
from .models import Employee,Role,Department,Employee_Experience,Employee_Education

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'salary', 'dept', 'role','bonus', 'phone', 'Join_date', 'email', 'emp_code')

# Register the models with enhanced admin configuration
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Employee_Education)
admin.site.register(Employee_Experience)
