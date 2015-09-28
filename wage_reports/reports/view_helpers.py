from django.http import HttpResponseRedirect, HttpResponse , JsonResponse
from django.shortcuts import get_object_or_404, render


from .forms import EmployeeForm , EmployeeMonthlyEntryForm , EmployerMonthlyEntryForm , UserCreateForm 
from .models import Monthly_employer_data, Monthly_employee_data, Employee , Employer , Locked_months


def get_single_entry_for_a_given_employee_and_month(employee , for_year , for_month):
    try:
        single_entry = Monthly_employee_data.objects.filter(employee=employee, for_year=for_year, for_month=for_month).latest('created')
        single_entry.has_data = True
        return single_entry
    except Monthly_employee_data.DoesNotExist:
        try:
            single_entry = Monthly_employee_data.objects.filter(employee=employee).latest('created')
            single_entry.has_data = True
            single_entry.is_approved = False
            single_entry.for_year = year_in_question
            single_entry.for_month = month_in_question
            return single_entry
        except Monthly_employee_data.DoesNotExist:
            empty_entry = Monthly_employee_data(employee=employee)
            empty_entry.has_data = False
            return empty_entry 

def edit_specific_entry_post(request , employee , entered_by):
    form_entry = EmployeeMonthlyEntryForm(request.POST)
    if form_entry.is_valid():
        partial_monthly_entree = form_entry.save(commit=False)
        partial_monthly_entree.employee = employee
        partial_monthly_entree.entered_by = entered_by
        #FIXME: Generate better error messages
        if partial_monthly_entree.save():
            return {
                'is_okay' : True
            }
        else:
            return {
                'is_okay' : True,
                'message' : 'Your input was not registerred. Make sure you have the permissions to enter this data at this time.'
            }

    else:
        return {
            'is_okay' : True,
            'message' : 'entry was not added, data was not valid'
        }
        

    

def edit_specific_entry_get(request , employee , error_message , action):
    try:
        single_entry = Monthly_employee_data.objects.filter(employee=employee).latest('created')
        form = EmployeeMonthlyEntryForm(instance=single_entry)
    except Monthly_employee_data.DoesNotExist:
        form = EmployeeMonthlyEntryForm()
    return render(request, 'reports/employee/monthly_entry.html' , { 'form' : form , 'employee_user_id' : employee.user.id , 'error_message': error_message , 'action':action})