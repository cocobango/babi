from django.contrib import admin

from .models import Monthly_employer_data, Monthly_employee_data, Monthly_system_data, Employee , Employer , Locked_months



# class ChoiceInline(admin.StackedInline):
#     model = Choice
#     extra = 3

# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#     ]
#     inlines = [ChoiceInline]

# admin.site.register(Question, QuestionAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    # fields = ('__all__',) 
    model = Employee
    list_display = ('employee' , 'is_approved', 'for_month' , 'for_year' , 'created' , 'gross_payment')

admin.site.register(Monthly_employee_data , EmployeeAdmin)

admin.site.register(Employee)
admin.site.register(Employer)


admin.site.register(Monthly_employer_data)
admin.site.register(Locked_months)
admin.site.register(Monthly_system_data)